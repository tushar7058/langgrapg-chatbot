# ⚡ LangGraph Agentic AI Chatbot

A production-ready, modular Agentic AI Assistant built with **LangGraph**, **Groq LLMs**, **Tavily Web Search**, and **Streamlit**.

---

## 🌟 Key Features & Use Cases

1. **💬 Basic Chatbot**: Fast, low-latency conversational assistant with multi-turn chat memory powered by Groq's high-performance inference engine.
2. **🌐 Chatbot with Web Search Tool**: Autonomous agent integrated with Tavily Search to retrieve real-time data, fact-check, and synthesize up-to-date answers.
3. **📰 AI News Researcher**: Specialized intelligence node providing structured tech briefings on recent AI breakthroughs, industry releases, and research papers.
4. **✍️ Blog Generation Agent**: End-to-end content strategist agent that generates comprehensive, SEO-optimized, highly structured blog articles.

---

## 📁 Project Structure

```
├── app.py                     # Main Streamlit execution entrypoint
├── pyproject.toml             # Project dependency definitions
├── requirements.txt           # Standard Python requirements
├── Dockerfile                 # Container deployment configuration
├── .env.example               # Template environment configuration
└── src/
    └── langgraphworkflow/
        ├── graph/             # LangGraph state machine & workflow builder
        ├── llms/              # LLM integration (Groq ChatGroq)
        ├── nodes/             # Modular agent workflow nodes
        ├── state/             # TypedDict graph state definitions
        ├── tools/             # Search and external tool integration
        └── ui/                # Streamlit UI, styling & config management
```

---

## 🚀 Quick Start

### 1. Clone & Setup Environment
```bash
# Using uv (Recommended)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or using standard pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy `.env.example` to `.env` and fill in your keys (or enter them directly in the Streamlit UI sidebar):
```bash
cp .env.example .env
```
- `GROQ_API_KEY`: [Get your free Groq key](https://console.groq.com/keys)
- `TAVILY_API_KEY`: [Get your free Tavily key](https://app.tavily.com/) *(Optional for web search)*

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Run with Docker
```bash
docker build -t langgraph-agentic-chatbot .
docker run -p 8501:8501 -e GROQ_API_KEY="your_key" langgraph-agentic-chatbot
```