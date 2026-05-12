# 🛡️ Self-Healing DevOps Agent

An autonomous infrastructure monitoring and remediation system that detects Docker container failures, diagnoses them using AI, and fixes them automatically, with zero human intervention.

> **Status:** 🚧 Actively building — Step 9 (Dockerise) in progress

---

## 💡 The Problem

When a Docker container crashes in production, someone has to:
- Notice it (usually via an alert at 3am)
- SSH into the server
- Read the logs
- Diagnose the issue
- Manually apply the right fix

**This takes 15–60 minutes and requires human attention.**

This agent removes that loop entirely.

---

## ✅ What It Does

| Without Agent | With Agent |
|---|---|
| Container crashes | Container crashes |
| Human gets paged | Agent detects in seconds |
| Human reads logs | LLM + error detection analyzes logs |
| Human applies fix | Agent applies smart fix based on error type |
| Human writes report | Incident saved to FAISS memory |
| Slack fills with noise | Only critical alerts sent to Slack |
| **15–60 minutes downtime** | **Under 30 seconds** |

---

## 🧠 Smart Error Detection

The agent doesn't just restart blindly. It detects the specific error type and applies the right fix:

| Error Type | Detection | Action |
|---|---|---|
| OOMKilled | Exit code 137 / OOMKilled flag | Increase memory limit → restart |
| Port conflict | "address already in use" in logs | Free port → restart |
| Clean exit | Exit code 0 | Simple restart |
| App crash | Exit code 1 + crash logs | Restart → Slack alert |
| Config error | Missing env vars in logs | Alert Slack for human review |
| Disk full | "no space left on device" | Docker prune → restart |
| Network error | "connection refused" in logs | Wait 10s → restart |
| Unknown | Any other failure | Restart → Slack alert |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Self-Healing Agent Loop                    │
│                                                             │
│  ┌──────────┐   ┌────────────────┐   ┌──────────────────┐   │
│  │ Monitor  │──▶│    Analyzer    │──▶│    Executor      │   │
│  │  Agent   │   │    Agent       │   │    Agent         │   │
│  │          │   │                │   │                  │   │
│  │ Detects  │   │ 1. Check FAISS │   │ SmartFix based   │   │
│  │ failed   │   │ 2. Detect error│   │ on error type    │   │
│  │containers│   │ 3. Save memory │   │ + Slack alerts   │   │
│  └──────────┘   └────────────────┘   └──────────────────┘   │
│                         │                      │            │
│                         ▼                      ▼            │
│              ┌────────────────┐    ┌─────────────────────┐  │
│              │  FAISS Memory  │    │   Langfuse Traces   │  │
│              │ Past incidents │    │ Full observability  │  │
│              └────────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| `Python 3.11` | Core language |
| `docker-py` | Docker container control |
| `CrewAI 1.14` | Multi-agent orchestration |
| `Groq (Llama 3.3 70B)` | LLM — fast, free inference |
| `FAISS` | Vector memory for past incidents |
| `Langfuse` | LLM observability & tracing |
| `Slack Webhooks` | Critical alerts to humans |
| `Ollama` | Local LLM fallback (llama3.2) |

---

## 📦 Project Structure

```
self-healing-agent/
├── src/
│   ├── main.py              ← Entry point + monitoring loop
│   └── crew/
│       ├── __init__.py
│       ├── agents.py        ← 3 CrewAI agents
│       ├── tasks.py         ← Task definitions
│       ├── tools.py         ← Docker + memory + Slack tools
│       └── memory.py        ← FAISS incident memory
├── memory/
│   ├── incidents.index      ← FAISS vector index
│   └── incidents.json       ← Incident history
├── .env                     ← API keys (never commit)
├── .gitignore
├── requirements.txt
├── Dockerfile               ← Coming Step 9
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker installed and running
- Groq API key (free at console.groq.com)
- Langfuse account (free at cloud.langfuse.com)
- Slack webhook (optional, for alerts)

### Installation

```bash
# Clone the repo
git clone https://github.com/niikkkhiil/Orchestrating_agent
cd self-healing-agent

# Create virtual environment
python3.11 -m venv orch
source orch/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

`.env` file:
```
OPENAI_API_KEY=dummy-not-used
GROQ_API_KEY=your-groq-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-key
LANGFUSE_SECRET_KEY=sk-lf-your-key
LANGFUSE_HOST=https://cloud.langfuse.com
SLACK_WEBHOOK_URL=https://hooks.slack.com/your-webhook
```

### Run the agent

```bash
cd src
python3 main.py
```

### Simulate a failure to test

```bash
# Terminal 1 — run the agent
python3 main.py

# Terminal 2 — simulate a container failure
docker stop test-nginx

# Watch Terminal 1 — agent detects, diagnoses, and fixes automatically
```

---

## 📊 Observability

Every scan is traced in Langfuse:
- Which agent ran and what it decided
- Token cost per incident
- Latency per agent
- Error type detected
- Fix applied

View your traces at: `cloud.langfuse.com`

---

## 🗺️ Roadmap

- [x] **Step 1** — List all Docker containers
- [x] **Step 2** — Detect unhealthy containers
- [x] **Step 3** — Auto-restart failed containers
- [x] **Step 4** — LLM-powered log analysis (Groq + Llama 3.3 70B)
- [x] **Step 5** — Continuous monitoring loop (5 min interval)
- [x] **Step 6** — CrewAI multi-agent system (Monitor + Analyzer + Executor)
- [x] **Step 7** — FAISS incident memory (check before LLM call)
- [x] **Step 8** — Langfuse observability (traces every scan)
- [x] **Step 8b** — Smart error detection (OOM, port conflict, crash, disk full)
- [x] **Step 8c** — Slack alerts for critical failures
- [ ] **Step 9** — Dockerise the agent (docker-compose)
- [ ] **Step 10** — CI/CD pipeline (GitHub Actions)

---

## 🤝 Contributing

This is a personal project — but PRs and feedback are welcome.

---

## 📄 License

MIT

---

> Built by [Nikhil Ganorkar](https://github.com/niikkkhiil) — DevOps & AI/ML Engineer
> Stack: Python · CrewAI · Groq · FAISS · Langfuse · Docker