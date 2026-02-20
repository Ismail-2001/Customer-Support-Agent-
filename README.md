<div align="center">

# 🤖 Nexus Support: Enterprise Multi-Agent Concierge
### A Production-Ready Customer Intelligence Platform Powered by LangGraph & DeepSeek

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Supervisor_Pattern-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![DeepSeek V3](https://img.shields.io/badge/DeepSeek_V3-Primary_Engine-6366F1?style=for-the-badge)](https://deepseek.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Premium_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-Service_Layer-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

<br/>

> *"Nexus doesn't just reply; it orchestrates a team of specialists to handle the most complex enterprise support workflows—autonomously."*

**Nexus Support** is an advanced, production-grade Customer Support platform built with a **Supervisor-Specialist architecture**. Leveraging **LangGraph** for stateful orchestration and **DeepSeek-V3** for high-reasoning intelligence, it features autonomous routing, real-time PII scrubbing, and a seamless Human-in-the-loop (HITL) escalation protocol.

[**✨ Features**](#-key-features) · [**🏗️ Architecture**](#-system-architecture) · [**🚀 Setup**](#-getting-started) · [**🛡️ Security**](#-security--safety)

---

</div>

## 📌 The Enterprise Support Gap

Traditional chatbots fail large-scale businesses because:

- **Rigid Decision Trees**: They can't handle non-linear customer journeys.
- **Context Blindness**: They lose track of identity and history across multiple inquiries.
- **Security Risks**: They lack integrated PII protection, exposing sensitive data to LLM logs.
- **No Escalation Path**: There's often no clean way to pause the AI when a human needs to step in.
- **Opacity**: Business owners can't see the real-time cost or "reasoning path" of the agent.

**Nexus Support solves these end-to-end.** It treats every interaction as a stateful graph traversal, prioritizing security and business intelligence at every node.

---

## ✨ Key Features

### 🧠 Supervisor-Specialist Orchestration
Instead of one generic agent, Nexus uses a **Central Supervisor** (`supervisor_node`) that analyzes user intent and delegates tasks to specialized specialists:
- **📦 Order Specialist**: Integrated with logistical databases to track real-time shipping and inventory.
- **⚙️ Tech Specialist**: Grounded troubleshooting using a localized technical knowledge base.
- **💳 Billing Specialist**: Handles complex financial inquiries and triggers escalation for disputes.
- **🌐 Generalist**: Manages top-of-funnel queries and identity qualification.

### 🛡️ Real-Time PII Scrubbing
Security is a first-class citizen in the `CustomerSupportAgent` class. An integrated **PII Sanitizer** uses high-performance regex patterns to mask:
- Emails: `[EMAIL_MASKED]`
- US Phone Numbers: `[PHONE_MASKED]`
- Sensitive Identifiers: Automatically filtered before hitting the LLM or the SQL database.

### 📊 Intelligence Analytics Console
A cinematic Streamlit sidebar provides real-time telemetry:
- **Active Operator**: Visually indicates which specialist (AI or Human) is currently in control.
- **Token Telemetry**: Live tracking of token consumption per session.
- **ROI Analytics**: Real-time cost estimation in USD ($) based on precise model pricing.
- **Infrastructure Health**: Visual status of the DeepSeek Engine, Postgres DB, and Security Layer.

### 🤝 Human-in-the-Loop (HITL) Escalation
When a query requires human intervention (e.g., a refund dispute), Nexus:
1. **Pauses the Graph**: Immediately locks the AI from further responses.
2. **Generates Ticket**: Automatically creates a prioritized entry in the `customer_database.py`.
3. **Locks Interface**: The UI switches to `is_human_takeover: True` mode, informing the user that assistant is paused while a human joins.

---

## 🏗️ System Architecture

### The LangGraph Flow

Nexus operates as a **Directed Acyclic Graph (DAG)** with conditional routing:

```text
┌──────────────────────────────────────────────────────────────────┐
│                      Nexus Intelligence Graph                    │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │
│  │ 1. IDENTIFY  │─────▶│ 2. SUPERVISOR│─────▶│ 3. SPECIALIST│    │
│  │              │      │              │      │              │    │
│  │• Extract ID  │      │• Analyze     │      │• Order Agent │    │
│  │• Check Tier  │      │  Intent      │      │• Tech Agent  │    │
│  │• Sentiment   │      │• Route Next  │      │• Billing Agnt│    │
│  └──────────────┘      └──────┬───────┘      └──────┬───────┘    │
│                               │                     │            │
│                               ▼                     ▼            │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │
│  │ 5. PERSIST   │◀─────│ 4. ESCALATE  │◀─────│     END      │    │
│  │              │      │              │      │              │    │
│  │• SQLite/PG   │      │• Lock UI     │      │• Wait for    │    │
│  │• Save Traces │      │• Create Tkt  │      │  User Input  │    │
│  └──────────────┘      └──────────────┘      └──────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### Module Breakdown

| File | Responsibility |
|---|---|
| `customer_support_agent.py` | The core LangGraph state machine and node definitions. |
| `customer_database.py` | SQLAlchemy layer for orders, customers, and ticket management. |
| `app.py` | Premium Streamlit UI with custom radial-gradient CSS and glassmorphism. |
| `api.py` | FastAPI gateway for integrating support into existing web platforms. |
| `dashboard.py` | Executive analytics for monitoring agent performance and cost. |

---

## 🚀 Getting Started

### Prerequisites

- **Python** `3.10+`
- **DeepSeek API Key** — [Get one here](https://platform.deepseek.com)
- **DeepSeek-V3 Model Access** (Default)

### 1. Clone & Install

```bash
git clone https://github.com/Ismail-2001/Customer-Support-Agent-.git
cd Customer-Support-Agent-
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
DEEPSEEK_API_KEY=your_deepseek_key_here
API_KEY=agentic_secret_key_2026
DATABASE_URL=sqlite:///customers.db
LOG_LEVEL=INFO
```

### 3. Launch the Terminal

Start the Backend API (FastAPI):
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8001
```

Start the Support Terminal (Streamlit):
```bash
python -m streamlit run app.py
```

Visit `http://localhost:8501` to start the session.

---

## 🛡️ Security & Safety

### PII Sanitization
The `_scrub_pii` method is executed at **both** entry points:
1. **Ingestion**: When a user message arrives, it is scrubbed before reaching the Graph.
2. **Storage**: All conversation traces are scrubbed again before being saved to SQLite/Postgres.

### Sliding Window Context
To prevent token bloat and hallucination, Nexus implements a **Sliding Window Memory** (`_trim_messages`) that maintains only the last 10 messages while preserving the core `SystemMessage` instructions.

### Dual-Model Fallback
Defined in `DualModelProvider`, Nexus includes a resiliency pattern that can automatically reroute requests to a secondary LLM provider if the primary (DeepSeek) experiences latency or outages.

---

## 🗺️ Roadmap

### ✅ Phase 1: Orchestration (Complete)
- [x] LangGraph Supervisor architecture
- [x] Specialist Specialist node isolation
- [x] Real-time PII Scrubbing
- [x] SQLAlchemy DB layer for Persistence

### 🔨 Phase 2: Knowledge Depth (Next)
- [ ] **Vector RAG**: Integration with ChromaDB/Pinecone for deep technical manual search.
- [ ] **Sentiment Routing**: Prioritize angry customers for immediate human escalation.
- [ ] **Email Integration**: Automated ticket responses via SendGrid.

### 🔭 Phase 3: Global Scale
- [ ] **Multi-Lingual Support**: Native translation nodes in the supervisor loop.
- [ ] **Webhooks**: Trigger external workflow automations (Zapier/Make).

---

<div align="center">

**Built for the high-reasoning era. Powered by LangGraph.**

*If Nexus Support helps your business scale, star ⭐ the repository.*

Built with ❤️ by [Ismail Sajid](https://github.com/Ismail-2001)

</div>
