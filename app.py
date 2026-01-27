# app.py

import streamlit as st
import time
import os
from datetime import datetime
from customer_support_agent import CustomerSupportAgent
from langchain_core.messages import HumanMessage, AIMessage

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Enterprise Support AI",
    page_icon="🛡️",
    layout="wide"
)

# --- PREMIUM CSS (Mobile-First) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="ViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    .main h1, .main p, .main span {
        color: #0f172a !important;
    }
    
    .stChatMessage {
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin: 1rem 0;
        max-width: 85%;
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        color: white;
    }
    
    .status-card {
        background: #1e293b;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
    
    .human-takeover {
        background: #fef2f2;
        border: 2px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        color: #b91c1c;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }

    /* Mobile Improvements */
    @media (max-width: 640px) {
        .main { padding: 0.5rem; }
        .stChatMessage { max-width: 95%; }
    }
</style>
""", unsafe_allow_html=True)

# --- INIT AGENT ---
@st.cache_resource
def load_agent():
    return CustomerSupportAgent()

agent = load_agent()

# --- SESSION STATE ---
if "state" not in st.session_state:
    st.session_state.state = None
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR (Expert BI Dashboard) ---
with st.sidebar:
    st.title("🛡️ Admin Console")
    st.markdown("---")
    
    if st.session_state.state:
        s = st.session_state.state
        st.subheader("📊 Agent Analytics")
        
        with st.container():
            st.markdown(f"""
            <div class="status-card">
                <small>ACTIVE SPECIALIST</small><br/>
                <b>{s.get('active_agent', 'Supervisor').replace('_',' ').title()}</b>
            </div>
            """, unsafe_allow_html=True)
            
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tier", s.get("customer_tier", "Standard").upper())
        with col2:
            st.metric("Tokens", f"{int(s.get('total_tokens', 0)):,}")

        # Cost Analysis (Expert Assessment 7)
        cost = s.get('total_tokens', 0) * 0.00000014
        st.write(f"💵 Est. Session Cost: **${cost:.6f}**")
        
        st.markdown("---")
        st.subheader("🌐 System Integrity")
        st.success("API: DeepSeek (Primary)")
        st.success("DB: SQLite (WAL-Mode)")
        st.info("Security: PII Scrubbing Active")

    if st.button("🗑️ Clear Session", use_container_width=True):
        st.session_state.state = None
        st.session_state.history = []
        st.rerun()

# --- MAIN CHAT ---
st.title("Enterprise AI Support")
st.caption("Secured, Multi-Agent Orchestration with Human Fail-safe")

# Auto-initialize Agent and Greeting
if st.session_state.state is None:
    with st.spinner("Initializing Enterprise Agents..."):
        st.session_state.state = agent.start_conversation()
        greeting = st.session_state.state["messages"][-1].content
        st.session_state.history.append({"role": "assistant", "content": greeting})
        st.rerun()

# Human Takeover Warning (Expert Assessment 5)
if st.session_state.state and st.session_state.state.get("is_human_takeover"):
    st.markdown('<div class="human-takeover">⚠️ AI PAUSED: A Human Specialist is taking over this session.</div>', unsafe_allow_html=True)

# Display History
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input (Disabled if human takeover active)
prompt = st.chat_input("How can we assist you today?", disabled=bool(st.session_state.state and st.session_state.state.get("is_human_takeover")))

if prompt:
    # 1. User Message
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Agent Execution
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Stream Graph
        for delta in agent.stream_message(st.session_state.state, prompt):
            for node, updated_state in delta.items():
                st.session_state.state = updated_state
                last_msg = updated_state["messages"][-1]
                if isinstance(last_msg, AIMessage):
                    full_response = last_msg.content
                    placeholder.markdown(full_response + " ▌")
        
        placeholder.markdown(full_response)
        st.session_state.history.append({"role": "assistant", "content": full_response})
    
    st.rerun()
