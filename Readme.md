**✨ Features**

🔍 Real-time Docker monitoring (docker-py CPU/memory stats)

🧠 RAG-powered diagnosis (Linkup API + FAISS local vector store)

👥 Multi-agent orchestration (CrewAI: Monitor → Analyzer → Planner → Executor)

⚡ Autonomous execution (Generates & applies docker-compose.yml)

💾 Persistent memory (MCP server tracks past fixes)

📊 Live dashboard (Streamlit UI + metrics)

🧪 Full test suite (85%+ coverage)


**🚀 Quickstart**

Prerequisites
Python 3.11+

Docker Desktop

Linkup.so free API key (1000 reqs/month)
8GB RAM (for Ollama)

bash
# 1. Clone & setup Python
git clone <your-repo> self-healing-devops-agent
cd self-healing-devops-agent
cp .env.example .env          # Add LINKUP_API_KEY=your_key_here
poetry install

# 2. Start local LLM (4.7GB download, 1x only)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.1:8b

# 3. Launch everything
docker-compose up -d           # Simulated infra (CPU spikes!)
uvicorn mcp.server:app --reload  # Memory server
streamlit run src/main.py      # 🎉 Agent UI ready!
Open: http://localhost:8501 → Click "🚨 CPU Alert"


**📋 Usage**

1. STREAMLIT: "Fix high CPU on web-app"
2. MONITOR: docker-py → "CPU=95%, 1 replica"
3. ANALYZER: Linkup scrapes Docker forums → "Use --scale flag"
4. PLANNER: Generates docker-compose.yml (replicas: 2)
5. EXECUTOR: docker-compose up --scale web-app=2
6. FIXED: CPU drops to 47% across 2 replicas
