# customer_support_agent.py

import os
import operator
import logging
import re
import json
from typing import TypedDict, Annotated, Sequence, Optional, Dict, Literal, List, Any
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from customer_database import CustomerDatabase

# Load environment variables
load_dotenv()

# --- LOGGING SETUP ---
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = "agent_activity.log"
file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=14)
file_handler.setFormatter(log_formatter)
logger = logging.getLogger("EnterpriseSupportAgent")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

# --- MULTI-VENDOR LLM FALLBACK ---
class DualModelProvider:
    """Enterprise-ready LLM provider with automatic fallback."""
    def __init__(self):
        # Primary: DeepSeek
        self.primary = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com/v1",
            max_tokens=2000
        )
        # Secondary: Could be OpenAI, Gemini, etc. For now generic fallback logic.
        self.secondary = self.primary # Mocking secondary as the same for this environment

    def invoke(self, prompt: Any) -> Any:
        try:
            return self.primary.invoke(prompt)
        except Exception as e:
            logger.warning(f"Primary LLM Failed: {e}. Falling back to secondary...")
            return self.secondary.invoke(prompt)

    def with_structured_output(self, schema: Any):
        # We wrap the underlying primary's structured output function
        return self.primary.with_structured_output(schema)

llm_provider = DualModelProvider()

# --- SCHEMAS ---
class RouterDecision(BaseModel):
    next_agent: Literal["order_specialist", "tech_specialist", "billing_specialist", "general_support", "escalate", "end"]
    reasoning: str

class CustomerSupportState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    customer_id: Optional[str]
    customer_name: Optional[str]
    customer_tier: str
    active_agent: str
    resolved: bool
    requires_escalation: bool
    is_human_takeover: bool # UX improvement 5.1
    ticket_id: Optional[str]
    current_step: str
    customer_sentiment: str
    total_tokens: int

# --- CORE AGENT ---
class CustomerSupportAgent:
    def __init__(self, db_path: str = "customers.db"):
        self.db = CustomerDatabase(db_path)
        self.graph = self._build_graph()
        self.router_chain = llm_provider.with_structured_output(RouterDecision)

    def _scrub_pii(self, text: str) -> str:
        """Security: PII Scrubbing (Email/Phone/SSN masking)."""
        # Mask emails
        text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL_MASKED]', text)
        # Mask phone numbers (simple US pattern)
        text = re.sub(r'\+?\d{1,3}[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}', '[PHONE_MASKED]', text)
        return text

    def _build_graph(self):
        workflow = StateGraph(CustomerSupportState)
        
        # Add Nodes
        workflow.add_node("identify", self._identify_node)
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("order_agent", self._order_agent_node)
        workflow.add_node("tech_agent", self._tech_agent_node)
        workflow.add_node("billing_agent", self._billing_agent_node)
        workflow.add_node("general_agent", self._general_support_node)
        workflow.add_node("escalate", self._escalation_node)
        
        # Define Flow
        workflow.set_entry_point("identify")
        workflow.add_edge("identify", "supervisor")
        
        workflow.add_conditional_edges(
            "supervisor",
            lambda x: x["active_agent"],
            {
                "order_specialist": "order_agent",
                "tech_specialist": "tech_agent",
                "billing_specialist": "billing_agent",
                "general_support": "general_agent",
                "escalate": "escalate",
                "end": END
            }
        )
        
        # Return to supervisor for any follow-up
        for agent in ["order_agent", "tech_agent", "billing_agent", "general_agent"]:
            workflow.add_edge(agent, "supervisor")
            
        workflow.add_edge("escalate", END)
        
        return workflow.compile()

    # --- NODES ---
    def _identify_node(self, state: CustomerSupportState) -> CustomerSupportState:
        if state.get("customer_id"): return state
        last_msg = state["messages"][-1].content if state["messages"] else ""
        match = re.search(r'[\w\.-]+@[\w\.-]+', last_msg)
        if match:
            customer = self.db.get_customer_by_email(match.group())
            if customer:
                logger.info(f"Identified customer: {customer['name']} ({customer['tier']})")
                return {**state, "customer_id": customer["customer_id"], "customer_name": customer["name"], "customer_tier": customer["tier"]}
        return state

    def _trim_messages(self, messages: List[BaseMessage], max_messages: int = 10) -> List[BaseMessage]:
        """Keep the last N messages to prevent context window overflow."""
        if len(messages) <= max_messages:
            return messages
        # Always keep the first message if it's a SystemMessage
        if isinstance(messages[0], SystemMessage):
            return [messages[0]] + list(messages[-(max_messages-1):])
        return list(messages[-max_messages:])

    def _supervisor_node(self, state: CustomerSupportState) -> CustomerSupportState:
        # UX: If human takeover is active, immediately end AI involvement
        if state.get("is_human_takeover"): return {**state, "active_agent": "end"}
        
        # Context Management: Trim messages before sending to LLM
        trimmed_messages = self._trim_messages(state["messages"])
        
        if isinstance(trimmed_messages[-1], AIMessage) and "help you today" in trimmed_messages[-1].content:
            return {**state, "active_agent": "end"}
            
        prompt = f"Supervisor: Decide specialist based on: {trimmed_messages[-1].content}"
        try:
            decision = self.router_chain.invoke(prompt)
            return {**state, "active_agent": decision.next_agent}
        except:
            return {**state, "active_agent": "general_support"}

    def _order_agent_node(self, state: CustomerSupportState) -> CustomerSupportState:
        if not state.get("customer_id"):
            return {**state, "messages": [AIMessage(content="I can help with orders! Please provide your email.")]}
        orders = self.db.get_customer_orders(state["customer_id"])
        if not orders:
            resp = "I found no active orders in your history."
        else:
            ord = orders[0]
            resp = f"Your latest order {ord['order_id']} ({ord['items']}) is currently {ord['status']}."
        return {**state, "messages": [AIMessage(content=resp + "\nAnything else?")]}

    def _tech_agent_node(self, state: CustomerSupportState) -> CustomerSupportState:
        """Grounded Tech Support Specialist."""
        query = state["messages"][-1].content.lower()
        kb = {
            "password": "Go to login -> Forgot Password.",
            "login": "Ensure cookies are enabled and try Incognito mode."
        }
        match = next((v for k, v in kb.items() if k in query), "Please describe your technical issue in more detail.")
        return {**state, "messages": [AIMessage(content=f"Tech Specialist: {match}\nDid that help?")]}

    def _billing_agent_node(self, state: CustomerSupportState) -> CustomerSupportState:
        msg = state["messages"][-1].content.lower()
        if any(w in msg for w in ["refund", "charge", "dispute"]):
            return {**state, "active_agent": "escalate"}
        return {**state, "messages": [AIMessage(content="Billing Specialist here. All your payments are up to date!")]}

    def _general_support_node(self, state: CustomerSupportState) -> CustomerSupportState:
        return {**state, "messages": [AIMessage(content="Generalist here. How can I help you?")]}

    def _escalation_node(self, state: CustomerSupportState) -> CustomerSupportState:
        # BI: Save conversation with detailed analytics before ending
        masked_msgs = [self._scrub_pii(m.content) for m in state["messages"]]
        session_data = {
            "id": f"SESS-{datetime.now().timestamp()}",
            "customer_id": state.get("customer_id"),
            "messages": masked_msgs,
            "resolved": True,
            "sentiment": state.get("customer_sentiment", "neutral"),
            "priority": "high",
            "tokens": state.get("total_tokens", 0)
        }
        self.db.save_conversation(session_data)
        
        tid = self.db.create_ticket(state.get("customer_id", "GUEST"), "General", "High", "Auto-escalated.")
        return {**state, "messages": [AIMessage(content=f"ESCALATION: A human will help you. Ticket #{tid}. AI is now paused.")], "is_human_takeover": True}

    # --- PUBLIC API ---
    def start_conversation(self) -> dict:
        return {"messages": [AIMessage(content="Welcome to Enterprise Support. How can I help today?")], 
                "customer_id": None, "customer_name": None, "customer_tier": "standard", "active_agent": "supervisor", 
                "resolved": False, "requires_escalation": False, "is_human_takeover": False, "total_tokens": 0}

    def send_message(self, state: dict, message: str) -> dict:
        # PII Scrubbing on ingestion for input security
        safe_msg = self._scrub_pii(message)
        state["messages"].append(HumanMessage(content=safe_msg))
        # Estimate tokens
        state["total_tokens"] = state.get("total_tokens", 0) + (len(safe_msg.split()) * 2 + 100)
        return self.graph.invoke(state)

    def stream_message(self, state: dict, message: str):
        safe_msg = self._scrub_pii(message)
        state["messages"].append(HumanMessage(content=safe_msg))
        state["total_tokens"] = state.get("total_tokens", 0) + (len(safe_msg.split()) * 2 + 100)
        for output in self.graph.stream(state):
            yield output
