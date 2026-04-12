from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
from environment import ModerationEnv
from models import Action
from grader import grade

app = FastAPI()

env = ModerationEnv()

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"

class StepRequest(BaseModel):
    action: str

class GraderRequest(BaseModel):
    task_data: dict
    action: str

@app.post("/reset")
async def reset(req: Optional[ResetRequest] = Body(default=None)):
    task = req.task if req and req.task else "easy"
    result = await env.reset(task)
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }

@app.post("/step")
async def step(req: StepRequest):
    result = await env.step(Action(action=req.action))
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }

@app.get("/state")
async def state():
    return await env.state()

@app.get("/tasks")
async def get_tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "description": "Binary classification of safe vs toxic content",
                "difficulty": "easy",
                "grader": "grader.grade",
                "max_attempts": 1,
                "scoring": "0.01-0.98 partial credit"
            },
            {
                "id": "medium",
                "description": "Multi-class classification (hate, spam, toxic, safe)",
                "difficulty": "medium",
                "grader": "grader.grade",
                "max_attempts": 1,
                "scoring": "0.01-0.98 partial credit"
            },
            {
                "id": "hard",
                "description": "Full moderation decision with severity and action",
                "difficulty": "hard",
                "grader": "grader.grade",
                "max_attempts": 1,
                "scoring": "0.01-0.98 partial credit"
            },
            {
                "id": "expert",
                "description": "Nuanced classification with label, decision, and severity",
                "difficulty": "expert",
                "grader": "grader.grade",
                "max_attempts": 1,
                "scoring": "0.01-0.98 partial credit"
            }
        ]
    }

@app.post("/grader")
async def run_grader(req: GraderRequest):
    score = grade(req.task_data, req.action)
    return {"score": score}

@app.get("/health")
async def health():
    return {"status": "ok"}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()