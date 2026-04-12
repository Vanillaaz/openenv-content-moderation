---
title: Openenv Content Moderation
emoji: "👁"
colorFrom: red
colorTo: gray
sdk: docker
app_port: 8000
tags:
  - openenv
pinned: false
---

# 🛡️ OpenEnv Content Moderation Environment

> A real-world, production-grade content moderation RL environment built on the OpenEnv framework by Meta & Hugging Face.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-blue)](https://github.com/meta-pytorch/OpenEnv)
[![HF Space](https://img.shields.io/badge/HuggingFace-Space-yellow)](https://huggingface.co/spaces/vanilla14/openenv-content-moderation)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)](https://fastapi.tiangolo.com/)

---

## 📌 Overview & Motivation

Content moderation is one of the most critical challenges in modern platforms. This environment simulates real-world moderation where an AI agent must:

* **Classify** content (`safe`, `toxic`, `hate`, `spam`)
* **Decide** moderation action (`approve`, `warn`, `remove`)
* **Assess** severity (`none`, `low`, `medium`, `high`)

### 💡 Use Cases

* 🧠 Reinforcement Learning training
* 🤖 LLM benchmarking
* 📊 Safety system research
* ⚙️ Agent evaluation across difficulty levels

---

## 🏗️ Project Structure

```
openenv-content-moderation/
│
├── app.py               # FastAPI server (main entrypoint)
├── environment.py       # Core environment logic
├── tasks.py             # Task datasets (easy/medium/hard/expert)
├── grader.py            # Reward / grading logic
├── models.py            # Pydantic models
├── inference.py         # Baseline agent script
│
├── openenv.yaml         # OpenEnv config
├── pyproject.toml       # Project metadata
├── Dockerfile           # Container setup
├── requirements.txt     # Dependencies
├── uv.lock              # Locked deps
│
└── server/
    ├── __init__.py
    └── app.py           # Server module entrypoint
```

---

## 🧪 Tasks

| Task     | Description                           | Difficulty  |
| -------- | ------------------------------------- | ----------- |
| `easy`   | Binary classification (safe vs toxic) | ⭐ Easy      |
| `medium` | Multi-class classification            | ⭐⭐ Medium   |
| `hard`   | Full moderation decision              | ⭐⭐⭐ Hard    |
| `expert` | Ambiguous nuanced content             | ⭐⭐⭐⭐ Expert |

---

## 👁️ Observation Space

```json
{
  "content": "user text",
  "task": "easy | medium | hard | expert"
}
```

---

## 🎯 Action Space

```
label=<label>;decision=<decision>;severity=<severity>
```

| Field    | Values                  |
| -------- | ----------------------- |
| label    | safe, toxic, hate, spam |
| decision | approve, warn, remove   |
| severity | none, low, medium, high |

---

## 🏆 Reward Function

* Label → +0.50
* Decision → +0.29
* Severity → +0.19

✔ Scores are clamped between **0.01 and 0.98**

---

## 🔌 API Endpoints

| Endpoint | Method | Description       |
| -------- | ------ | ----------------- |
| /reset   | POST   | Start new episode |
| /step    | POST   | Submit action     |
| /state   | GET    | Current state     |
| /tasks   | GET    | List tasks        |
| /grader  | POST   | Score action      |
| /health  | GET    | Health check      |
| /docs    | GET    | Swagger UI        |

---

## ⚙️ Local Setup

```bash
git clone https://github.com/Vanillaaz/openenv-content-moderation.git
cd openenv-content-moderation

pip install -r requirements.txt

uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

👉 Open: http://localhost:8000/docs

---

## 🐳 Docker

```bash
docker build -t openenv-content-moderation .
docker run -p 8000:8000 openenv-content-moderation
```

---

## 🤖 Running the Agent

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="your_token"

python inference.py
```

---

## 🔐 Environment Variables

| Variable     | Description      |
| ------------ | ---------------- |
| API_BASE_URL | LLM endpoint     |
| MODEL_NAME   | Model used       |
| HF_TOKEN     | Hugging Face key |

---

## 🌐 Live Demo

* HF Space: https://huggingface.co/spaces/vanilla14/openenv-content-moderation
* API Docs: https://vanilla14-openenv-content-moderation.hf.space/docs
* Health: https://vanilla14-openenv-content-moderation.hf.space/health

---

## 👩‍💻 Author

**Venisha Dsouza**
Built for **OpenEnv Hackathon 🚀**
