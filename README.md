# 🛡️ Self-Healing DevOps Agent

An autonomous infrastructure monitoring and remediation system that detects Docker container failures and fixes them automatically — with zero human intervention.

> **Status:** 🚧 In Progress — actively building

---

## 💡 The Problem

When a Docker container crashes in production, someone has to:
- Notice it (usually via an alert at 3am)
- SSH into the server
- Read the logs
- Diagnose the issue
- Manually restart or fix it

**This takes 15–60 minutes and requires human attention.**

This agent removes that loop entirely.

---

## ✅ What It Does

| Without Agent | With Agent |
|---|---|
| Container crashes | Container crashes |
| Human gets paged | Agent detects in seconds |
| Human reads logs | LLM analyzes logs |
| Human applies fix | Agent applies fix |
| Human writes report | Incident logged to memory |
| **15–60 minutes downtime** | **Under 5 seconds** |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                Self-Healing Agent Loop               │
│                                                      │
│  ┌─────────┐    ┌──────────┐    ┌─────────────────┐ │
│  │ Monitor │───▶│ Analyzer │───▶│    Executor     │ │
│  │  Agent  │    │  Agent   │    │     Agent       │ │
│  │         │    │  (LLM)   │    │                 │ │
│  │ Watches │    │ Diagnoses│    │ Restarts/Fixes  │ │
│  │ Docker  │    │  failure │    │   container     │ │
│  └─────────┘    └──────────┘    └─────────────────┘ │
│                      │                   │           │
│                      ▼                   ▼           │
│               ┌────────────────────────────────┐    │
│               │     Memory (FAISS + MCP)        │    │
│               │  Stores past incidents & fixes  │    │
│               └────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| `Python` | Core language |
| `docker-py` | Docker container control |
| `OpenAI API` | LLM-powered failure analysis |
| `CrewAI` | Multi-agent orchestration |
| `FAISS` | Vector memory for past incidents |
| `MCP` | Persistent memory protocol |
| `Langfuse` | LLM observability & tracing |

---

## 📦 Project Structure

```
self-healing-agent/
├── src/
│   ├── agents.py          # Monitor + Executor agents
│   ├── analyzer.py        # LLM diagnosis (coming)
│   ├── memory.py          # FAISS + MCP memory (coming)
│   └── observability.py   # Langfuse tracing (coming)
├── tests/
│   └── golden_cases/      # 30 eval test cases (coming)
├── docker-compose.yml     # Test environment
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker installed and running
- OpenAI API key (for Step 4+)

### Installation

```bash
# Clone the repo
git clone https://github.com/niikkkhiil/self-healing-agent
cd self-healing-agent

# Create virtual environment
python3 -m venv orch
source orch/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the agent

```bash
cd src
python3 agents.py
```

### Test it — simulate a failure

```bash
# Terminal 1 — start a test container
docker run -d --name test-nginx nginx

# Terminal 2 — run the agent
python3 agents.py

# Now stop the container to simulate a crash
docker stop test-nginx

# Run the agent again — it detects and fixes automatically
python3 agents.py
```

---

## 🗺️ Roadmap

- [x] **Step 1** — List all running Docker containers
- [x] **Step 2** — Detect unhealthy/exited containers
- [x] **Step 3** — Auto-restart failed containers
- [x] **Step 4** — LLM-powered failure analysis (OpenAI)
- [ ] **Step 5** — Multi-agent architecture (CrewAI)
- [ ] **Step 6** — Incident memory (FAISS + MCP)
- [ ] **Step 7** — Full observability (Langfuse + eval suite)
- [ ] **Step 8** — CI/CD pipeline + Docker deployment

---

## 📊 Observability (Coming — Step 7)

Every agent action will be traced with Langfuse:
- Token cost per incident
- Latency per agent
- Fix success rate
- 30 golden test cases with regression gates

---

## 🤝 Contributing

This is a personal learning project — but PRs and feedback are welcome.

---

## 📄 License

MIT

---

> Built by [Nikhil Ganorkar](https://github.com/niikkkhiil) — DevOps & AI/ML Engineer
> Part of learning journey: Python → FastAPI → LLM Engineering → Agentic Systems
