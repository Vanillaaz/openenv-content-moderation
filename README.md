---

title: OpenEnv Content Moderation
emoji: 🛡️
colorFrom: red
colorTo: gray
sdk: docker
app_port: 8000
tags:

* openenv
  pinned: false

---

# 🛡️ OpenEnv Content Moderation Environment

A **production-style reinforcement learning environment** for content moderation, built using the **OpenEnv framework** by Meta & Hugging Face.

This environment simulates real-world moderation pipelines where an AI agent must classify, evaluate, and take action on user-generated content.

---

## 📌 Overview & Motivation

Content moderation remains one of the most complex challenges in modern AI systems. Platforms like Meta, YouTube, and X must continuously detect:

* Toxic language
* Hate speech
* Spam and manipulation
* Subtle or sarcastic harmful content

This environment recreates that challenge in a structured RL setting.

### 🎯 Agent Responsibilities

At every step, the agent must:

1. **Classify** content → (`safe`, `toxic`, `hate`, `spam`)
2. **Decide** action → (`approve`, `warn`, `remove`)
3. **Assess** severity → (`none`, `low`, `medium`, `high`)

---

## 🏗️ Project Structure

```
openenv-content-moderation/
│
├── app.py               # FastAPI entrypoint
├── environment.py       # Core ModerationEnv logic
├── tasks.py             # Task datasets
├── grader.py            # Reward logic
├── models.py            # Pydantic schemas
├── inference.py         # Baseline agent
├── openenv.yaml         # OpenEnv config
├── Dockerfile           # Container setup
├── requirements.txt     # Dependencies
└── server/
    └── app.py           # Server module
```

---

## 🧪 Tasks

| Task   | Description                                   | Difficulty  |
| ------ | --------------------------------------------- | ----------- |
| easy   | Binary classification (safe vs toxic)         | ⭐ Easy      |
| medium | Multi-class classification                    | ⭐⭐ Medium   |
| hard   | Full moderation (label + decision + severity) | ⭐⭐⭐ Hard    |
| expert | Ambiguous, nuanced real-world content         | ⭐⭐⭐⭐ Expert |

---

## 👁️ Observation Space

```json
{
  "content": "User-generated text",
  "task": "easy | medium | hard | expert"
}
```

---

## 🎯 Action Space

Agent must return a **strictly formatted string**:

```
label=<label>;decision=<decision>;severity=<severity>
```

### Allowed Values

| Field    | Values                  |
| -------- | ----------------------- |
| label    | safe, toxic, hate, spam |
| decision | approve, warn, remove   |
| severity | none, low, medium, high |

### Example

```
label=toxic;decision=warn;severity=medium
```

---

## 🏆 Reward Function

Partial credit is awarded:

| Component | Reward |
| --------- | ------ |
| Label     | +0.50  |
| Decision  | +0.29  |
| Severity  | +0.19  |

* Scores are clamped between **0.01 and 0.98**
* Encourages learning even from partial correctness

---

## 🔌 API Endpoints

| Endpoint | Method | Description       |
| -------- | ------ | ----------------- |
| /reset   | POST   | Start new episode |
| /step    | POST   | Submit action     |
| /state   | GET    | Get current state |
| /tasks   | GET    | List tasks        |
| /grader  | POST   | Evaluate action   |
| /health  | GET    | Health check      |
| /docs    | GET    | Swagger UI        |

---

## ⚙️ Local Setup

### Requirements

* Python 3.10+
* pip

```bash
git clone https://github.com/Vanillaaz/openenv-content-moderation.git
cd openenv-content-moderation

pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

👉 Open: http://localhost:8000/docs

---

## 🐳 Docker Setup

```bash
docker build -t openenv-content-moderation .
docker run -p 8000:8000 openenv-content-moderation
```

---

## 🤖 Baseline Agent

Uses:

* Model: `Qwen/Qwen2.5-72B-Instruct`
* API: Hugging Face Router

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="your_token"

python inference.py
```

---

## 📊 Expected Performance

| Task   | Score Range |
| ------ | ----------- |
| easy   | 0.50 – 0.98 |
| medium | 0.50 – 0.98 |
| hard   | 0.50 – 0.79 |
| expert | 0.01 – 0.79 |

---

## 🔐 Environment Variables

| Variable     | Description          |
| ------------ | -------------------- |
| API_BASE_URL | LLM endpoint         |
| MODEL_NAME   | Model name           |
| HF_TOKEN     | Hugging Face API key |

---

## 🌐 Live Deployment

* 🤗 HF Space:
  https://huggingface.co/spaces/vanilla14/openenv-content-moderation

* 📖 API Docs:
  https://vanilla14-openenv-content-moderation.hf.space/docs

* ❤️ Health Check:
  https://vanilla14-openenv-content-moderation.hf.space/health

---

## 👩‍💻 Author

**Venisha Dsouza**
Built for the **Meta PyTorch OpenEnv Hackathon** 🚀

---

## 📄 License

MIT License
