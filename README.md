# 🚀 OpenEnv Content Moderation Environment

An AI-powered content moderation environment built for evaluating and classifying user-generated text across multiple difficulty levels.

---

## 📌 Overview

This project simulates a **moderation environment** where an agent must analyze text and take appropriate actions such as labeling toxicity, determining severity, and making moderation decisions.

It is designed for:

* 🧠 Reinforcement Learning environments
* 🤖 AI moderation systems
* ⚙️ API-based evaluation pipelines

---

## ✨ Features

* 🟢 **Easy Mode**
  Binary classification → `safe` vs `toxic`

* 🟡 **Medium Mode**
  Multi-class classification → `hate`, `spam`, `toxic`, `safe`

* 🔴 **Hard Mode**
  Full moderation decision → label + severity + action

* ⚡ **FastAPI Backend**
  Clean and scalable API endpoints

* 🐳 **Dockerized Deployment**
  Easily deployable on Hugging Face Spaces

* 🔐 **Secure API Key Handling**
  Environment variables and secrets supported

---

## 🏗️ Project Structure

```
openenv-moderation/
│
├── environment.py     # Core environment logic
├── tasks.py           # Dataset for tasks
├── grader.py          # Reward evaluation logic
├── models.py          # Data models (Pydantic)
├── inference.py       # AI interaction logic
├── server.py          # FastAPI server
├── server/
│   ├── __init__.py    # empty file
│   └── app.py         # main
├── main.py            # Local testing
├── Dockerfile         # Container setup
├── requirements.txt   # Dependencies
└── openenv.yaml       # Environment config
```

---

## 🔌 API Endpoints

### ▶️ Reset Environment

```http
POST /reset
```

**Request:**

```json
{
  "task": "easy"
}
```

---

### ▶️ Take a Step

```http
POST /step
```

**Request:**

```json
{
  "action": "label=toxic"
}
```

---

### ▶️ Get Current State

```http
GET /state
```

---

## 🧪 Example Workflow

1. Reset environment
2. Receive observation
3. Send action
4. Get reward

```json
{
  "observation": {
    "content": "You are stupid",
    "task": "easy"
  },
  "reward": 1.0,
  "done": true
}
```

---

## 🌐 Live Demo

👉 Hugging Face Space:
https://huggingface.co/spaces/vanilla14/openenv-content-moderation

👉 API Docs:
https://vanilla14-openenv-content-moderation.hf.space/docs

---

## ⚙️ Setup (Local)

```bash
# Clone repo
git clone https://github.com/yourusername/openenv-moderation.git

# Navigate
cd openenv-moderation

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn server:app --reload
```

---

## 🔐 Environment Variables

| Variable       | Description              |
| -------------- | ------------------------ |
| OPENAI_API_KEY | API key for model access |
| API_BASE_URL   | Hugging Face router URL  |
| MODEL_NAME     | Model used for inference |

---

## 🧠 Tech Stack

* Python 🐍
* FastAPI ⚡
* Docker 🐳
* Hugging Face Spaces 🤗
* OpenAI-compatible APIs

---

## 🎯 Use Cases

* AI moderation systems
* RL training environments
* Safety benchmarking
* Hackathon projects

---

## 👩‍💻 Author

**Venisha Dsouza**
Built as part of an AI hackathon 🚀

---

## ⭐ Final Note

This project demonstrates how AI can be used to build **scalable, real-time content moderation systems** with structured evaluation and deployment.

If you found this useful, consider giving it a ⭐!
