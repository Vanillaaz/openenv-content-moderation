```markdown
# 🚀 OpenEnv Content Moderation Environment

A real-world content moderation RL environment built on the OpenEnv framework. An AI agent analyzes user-generated text and makes moderation decisions across multiple difficulty levels.

---

## 📌 Overview

This environment simulates a **content moderation pipeline** where an agent must classify text, determine severity, and make moderation decisions.

Built for:
* 🧠 Reinforcement Learning training and evaluation
* 🤖 AI moderation benchmarking
* ⚙️ OpenEnv-compatible agent evaluation

---

## 🏗️ Project Structure

```
openenv-content-moderation/
│
├── app.py             # FastAPI server (main entrypoint)
├── environment.py     # Core ModerationEnv logic
├── tasks.py           # Task datasets (easy/medium/hard/expert)
├── grader.py          # Reward/grading logic (0.01–0.98)
├── models.py          # Pydantic models (Action, Observation, StepResult)
├── inference.py       # Baseline LLM agent script
├── openenv.yaml       # OpenEnv environment config
├── pyproject.toml     # Project dependencies
├── Dockerfile         # Container setup
├── requirements.txt   # Python dependencies
├── uv.lock            # Locked dependencies
└── server/
    ├── __init__.py
    └── app.py
```

---

## 🧪 Tasks

| Task | Description | Difficulty |
|------|-------------|------------|
| `easy` | Binary classification: `safe` vs `toxic` | Easy |
| `medium` | Multi-class: `hate`, `spam`, `toxic`, `safe` | Medium |
| `hard` | Full decision: label + decision + severity | Hard |
| `expert` | Nuanced content with subtle violations | Expert |

---

## 🎯 Action Space

Actions must follow this exact format:

```
label=<label>;decision=<decision>;severity=<severity>
```

| Field | Values |
|-------|--------|
| `label` | `safe`, `toxic`, `hate`, `spam` |
| `decision` | `approve`, `warn`, `remove` |
| `severity` | `none`, `low`, `medium`, `high` |

Example:
```
label=toxic;decision=warn;severity=medium
```

---

## 👁️ Observation Space

```json
{
  "content": "string — the text content to moderate",
  "task": "string — easy | medium | hard | expert"
}
```

---

## 🏆 Reward Function

| Component | Points | Condition |
|-----------|--------|-----------|
| Correct label | +0.50 | label matches expected |
| Correct decision | +0.29 | decision matches expected |
| Correct severity | +0.19 | severity matches expected |

Scores are clamped strictly between **0.01 and 0.98** (never exact 0 or 1).

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset` | POST | Start new episode |
| `/step` | POST | Submit moderation decision |
| `/state` | GET | Get current episode state |
| `/tasks` | GET | List all tasks with graders |
| `/grader` | POST | Score an action directly |
| `/health` | GET | Health check |

### Reset
```http
POST /reset
Content-Type: application/json

{"task": "easy"}
```

### Step
```http
POST /step
Content-Type: application/json

{"action": "label=toxic;decision=warn;severity=medium"}
```

---

## ⚙️ Setup (Local)

```bash
# Clone repo
git clone https://github.com/Vanillaaz/openenv-content-moderation.git
cd openenv-content-moderation

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | LLM API endpoint | `https://router.huggingface.co/v1` |
| `MODEL_NAME` | Model for inference | `Qwen/Qwen2.5-72B-Instruct` |
| `HF_TOKEN` | Hugging Face API key | None (required) |

---

## 🐳 Docker

```bash
docker build -t openenv-content-moderation .
docker run -p 8000:8000 openenv-content-moderation
```

---

## 🌐 Live Demo

👉 HF Space: https://huggingface.co/spaces/vanilla14/openenv-content-moderation  
👉 API Docs: https://vanilla14-openenv-content-moderation.hf.space/docs  
👉 Tasks: https://vanilla14-openenv-content-moderation.hf.space/tasks

---

## 🧠 Baseline Scores

| Task | Score Range |
|------|-------------|
| easy | 0.50 – 0.98 |
| medium | 0.50 – 0.98 |
| hard | 0.50 – 0.98 |
| expert | 0.50 – 0.98 |

---

## 👩‍💻 Author

**Venisha Dsouza** — Built for the Meta PyTorch OpenEnv Hackathon 🚀
```

If you found this useful, consider giving it a ⭐!
