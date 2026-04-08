from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from environment import ModerationEnv
from models import Action

app = FastAPI()
env = ModerationEnv()

# ----------- REQUEST MODELS -----------

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"

class StepRequest(BaseModel):
    action: str


# ----------- ENDPOINTS -----------

@app.post("/reset")
async def reset(req: Optional[ResetRequest] = None):
    task = req.task if req else "easy"

    result = await env.reset(task)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }


@app.post("/step")
async def step(req: StepRequest):
    action = Action(action=req.action)

    result = await env.step(action)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }


@app.get("/state")
async def state():
    return await env.state()