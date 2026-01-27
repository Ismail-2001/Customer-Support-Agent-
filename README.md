# 🤖 Enterprise AI Customer Support Agent (LangGraph)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Framework-LangGraph-orange)](https://github.com/langchain-ai/langgraph)

An advanced, production-ready Multi-Agent Customer Support system powered by **LangGraph** and **DeepSeek AI**. This project demonstrates a sophisticated "Supervisor-Specialist" architecture capable of autonomous routing, PII scrubbing, real-time analytics, and human-in-the-loop escalation. Built for businesses that require high-accuracy automated support with enterprise-grade security.

---

## ✨ Key Features

- **🧠 Multi-Agent Orchestration**: Uses a central **Supervisor Agent** to dynamically route queries to specialized specialists (Order, Billing, Technical, General).
- **🛡️ Enterprise Security**: Integrated **PII Scrubbing** engine masks sensitive data (Emails, Phone Numbers) before processing and storage.
- **📉 Real-time Token & Cost Tracking**: Built-in analytics dashboard showing live $ cost estimation and token usage per session.
- **🤝 Human-in-the-Loop**: Intelligent escalation logic that "pauses" the AI and locks the chat interface when a human specialist is required.
- **⚡ Streaming UI**: Modern Streamlit interface with real-time response streaming for reduced perceived latency.
- **🐘 Scalable Persistence**: Dual-mode database support (SQLite with WAL-mode for local dev, PostgreSQL for production scaling).
- **🔄 Fault Tolerance**: Implementation of a global `error_handler` node and LLM fallback strategies.

---

## 🛠 Tech Stack

- **Core Framework**: Python 3.11+, [LangGraph](https://github.com/langchain-ai/langgraph)
- **Large Language Model**: [DeepSeek AI](https://deepseek.com/) (OpenAI-compatible SDK)
- **API Interface**: [FastAPI](https://fastapi.tiangolo.com/) with Uvicorn
- **Frontend UI**: [Streamlit](https://streamlit.io/)
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Infrastructure**: Docker & Docker Compose

---

## 🏗 Architecture

The system follows a **Directed Acyclic Graph (DAG)** workflow:

1. **Identify Node**: Extracts customer identity and tier from context.
2. **Supervisor (Router)**: Analyzes user intent using structured Pydantic outputs and delegates to the appropriate specialist.
3. **Specialist Team**:
   - **Order Specialist**: Queries logistics database for tracking.
   - **Technical Specialist**: Grounded troubleshooting via local KB.
   - **Billing Specialist**: Handles financial inquiries and escalation triggers.
4. **Safety Layer**: Centralized PII scrubbing and context window trimming (Sliding Window: 10 messages).

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- [DeepSeek API Key](https://platform.deepseek.com/)
- Docker (optional, for containerized run)

### Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/langgraph-support-agent.git
   cd langgraph-support-agent
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   DEEPSEEK_API_KEY=your_api_key_here
   API_KEY=agentic_secret_key_2026
   DATABASE_URL=customers.db  # Use postgres:// for production
   LOG_LEVEL=INFO
   ```

---

## 📖 Usage

### Running Locally

**Start the Backend API:**
```bash
py -m uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

**Start the Streamlit UI:**
```bash
py -m streamlit run app.py --server.port 8503
```

- **Chat Interface**: `http://localhost:8503`
- **Interactive API Docs**: `http://localhost:8001/docs`

---

## 🐳 Deployment

### Using Docker Compose
The easiest way to run the production stack locally is via Docker:

```bash
docker-compose up --build
```
This spins up both the FastAPI backend and the Streamlit frontend in isolated containers.

---

## 📸 Screenshots / Demo

> *Placeholder: Add your UI screenshots here*
- **Sidebar Analytics**: [Image]
- **Specialist Switching**: [Image]
- **Human Takeover State**: [Image]

---

## 🗺 Roadmap

- [ ] **Vector RAG Integration**: Replace keyword search with ChromaDB/Pinecone for technical documentation.
- [ ] **Multi-Model Fallback**: Automated switching to GPT-4o if DeepSeek latency exceeds thresholds.
- [ ] **Voice Support**: Twilio integration for automated IVR support.
- [ ] **LangSmith Tracing**: Deep observability for agentic reasoning paths.

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Built with ❤️ for the Agentic AI Community.**
