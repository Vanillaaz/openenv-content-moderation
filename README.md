Here's your complete final README.md — copy and paste this entire thing:

```markdown
---
title: Openenv Content Moderation
emoji: 👁
colorFrom: red
colorTo: gray
sdk: docker
app_port: 8000
tags:
  - openenv
pinned: false
---

# 🛡️ OpenEnv Content Moderation Environment

> A real-world, production-grade content moderation RL environment built on the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework by Meta & Hugging Face.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-blue)](https://github.com/meta-pytorch/OpenEnv)
[![HF Space](https://img.shields.io/badge/HuggingFace-Space-yellow)](https://huggingface.co/spaces/vanilla14/openenv-content-moderation)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)](https://fastapi.tiangolo.com/)

---

## 📌 Overview & Motivation

Content moderation is one of the most critical and costly challenges facing modern platforms. Companies like Meta, Twitter, and YouTube spend billions of dollars annually trying to detect toxic, hateful, and harmful content at scale — yet the problem remains largely unsolved.

This environment simulates that exact challenge. An AI agent is presented with user-generated text and must:
- **Classify** the content type (safe, toxic, hate, spam)
- **Decide** the appropriate moderation action (approve, warn, remove)
- **Assess** the severity (none, low, medium, high)

This makes it ideal for:
- 🧠 Training RL agents on real-world decision-making tasks
- 🤖 Benchmarking LLM content moderation capabilities
- ⚙️ Evaluating agent performance across increasing difficulty levels
- 📊 Research into automated content safety systems

---

## 🏗️ Project Structure

```
openenv-content-moderation/
│
├── app.py             # FastAPI server (main entrypoint)
├── environment.py     # Core ModerationEnv logic
├── tasks.py           # Task datasets (easy/medium/hard/expert)
├── grader.py          # Deterministic reward/grading logic
├── models.py          # Pydantic models (Action, Observation, StepResult)
├── inference.py       # Baseline LLM agent script
├── openenv.yaml       # OpenEnv environment configuration
├── pyproject.toml     # Project metadata and dependencies
├── Dockerfile         # Container definition
├── requirements.txt   # Python dependencies
├── uv.lock            # Locked dependency tree
└── server/
    ├── __init__.py
    └── app.py         # Server module entrypoint
```

---

## 🧪 Tasks

| Task | Description | Difficulty | Grader |
|------|-------------|------------|--------|
| `easy` | Binary classification — is the content `safe` or `toxic`? | ⭐ Easy | `grader.grade` |
| `medium` | Multi-class classification — `hate`, `spam`, `toxic`, or `safe` | ⭐⭐ Medium | `grader.grade` |
| `hard` | Full moderation decision — label + decision + severity | ⭐⭐⭐ Hard | `grader.grade` |
| `expert` | Nuanced, ambiguous content requiring deep contextual understanding | ⭐⭐⭐⭐ Expert | `grader.grade` |

### Task Difficulty Progression

- **Easy**: Obvious content — clear safe or toxic signals, no ambiguity
- **Medium**: Requires understanding of hate speech and spam patterns
- **Hard**: Requires full moderation pipeline — label, action, and severity all matter
- **Expert**: Subtle, sarcastic, or culturally nuanced content that challenges frontier models

---

## 👁️ Observation Space

Each episode provides the agent with the following observation:

```json
{
  "content": "string — the user-generated text to moderate",
  "task": "string — one of: easy | medium | hard | expert"
}
```

---

## 🎯 Action Space

The agent must respond with a structured action string in **exactly** this format:

```
label=<label>;decision=<decision>;severity=<severity>
```

| Field | Allowed Values | Description |
|-------|---------------|-------------|
| `label` | `safe`, `toxic`, `hate`, `spam` | Content category |
| `decision` | `approve`, `warn`, `remove` | Moderation action |
| `severity` | `none`, `low`, `medium`, `high` | Severity level |

### Example Actions
```
label=safe;decision=approve;severity=none
label=toxic;decision=warn;severity=medium
label=hate;decision=remove;severity=high
label=spam;decision=remove;severity=low
```

---

## 🏆 Reward Function

The grader provides **partial credit** — agents are rewarded for each correct component:

| Component | Reward | Condition |
|-----------|--------|-----------|
| Correct `label` | +0.50 | Label matches expected value |
| Correct `decision` | +0.29 | Decision matches expected value |
| Correct `severity` | +0.19 | Severity matches expected value |

> All scores are clamped strictly between **0.01 and 0.98** — never exact 0.0 or 1.0.

**Maximum possible score per episode: 0.98**

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset` | POST | Start a new episode |
| `/step` | POST | Submit a moderation decision |
| `/state` | GET | Get current episode state |
| `/tasks` | GET | List all tasks with grader info |
| `/grader` | POST | Score an action without a full episode |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive Swagger API docs |

### Reset Episode
```http
POST /reset
Content-Type: application/json

{"task": "easy"}
```

**Response:**
```json
{
  "observation": {
    "content": "You are stupid and ugly",
    "task": "easy"
  },
  "reward": 0.0,
  "done": false
}
```

### Submit Action
```http
POST /step
Content-Type: application/json

{"action": "label=toxic;decision=warn;severity=low"}
```

**Response:**
```json
{
  "observation": {
    "content": "You are stupid and ugly",
    "task": "easy"
  },
  "reward": 0.79,
  "done": true
}
```

---

## 📊 Baseline Scores

Baseline agent: `Qwen/Qwen2.5-72B-Instruct` via Hugging Face Router

| Task | Score Range | Notes |
|------|-------------|-------|
| `easy` | 0.50 – 0.98 | High accuracy on obvious content |
| `medium` | 0.50 – 0.98 | Good on hate/spam detection |
| `hard` | 0.50 – 0.79 | Struggles with severity calibration |
| `expert` | 0.01 – 0.79 | Nuanced cases challenge frontier models |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- pip or uv

```bash
# Clone the repository
git clone https://github.com/Vanillaaz/openenv-content-moderation.git
cd openenv-content-moderation

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open: http://localhost:8000/docs

---

## 🐳 Docker

```bash
# Build the image
docker build -t openenv-content-moderation .

# Run the container
docker run -p 8000:8000 openenv-content-moderation
```

Then open: http://localhost:8000/docs

---

## 🤖 Running the Baseline Agent

```bash
# Set environment variables
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="your_hf_token_here"

# Run inference across all tasks
python inference.py
```

Expected output:
```
[START] task=easy env=content-moderation model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=label=safe;decision=approve;severity=none reward=0.98 done=true error=null
[END] success=true steps=1 score=0.98 rewards=0.98
```

---

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | LLM API endpoint URL | `https://router.huggingface.co/v1` |
| `MODEL_NAME` | Model identifier for inference | `Qwen/Qwen2.5-72B-Instruct` |
| `HF_TOKEN` | Hugging Face API key | *(required, no default)* |

---

## 🌐 Live Demo

| Link | URL |
|------|-----|
| 🤗 HF Space | https://huggingface.co/spaces/vanilla14/openenv-content-moderation |
| 📖 API Docs | https://vanilla14-openenv-content-moderation.hf.space/docs |
| ✅ Tasks | https://vanilla14-openenv-content-moderation.hf.space/tasks |
| ❤️ Health | https://vanilla14-openenv-content-moderation.hf.space/health |

---

## 👩‍💻 Author

**Venisha Dsouza** — Built for the **Meta PyTorch OpenEnv Hackathon** x Scaler School of Technology 🚀

---

## 📄 License

MIT License — feel free to use, modify, and build on this environment.
```
