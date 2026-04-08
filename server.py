from fastapi import FastAPI, Body
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

# RESET - accepts optional body with task field
@app.post("/reset")
async def reset(req: Optional[ResetRequest] = Body(default=None)):
    task = req.task if req and req.task else "easy"
    result = await env.reset(task)
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }

# STEP
@app.post("/step")
async def step(req: StepRequest):
    result = await env.step(Action(action=req.action))
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }

# STATE
@app.get("/state")
async def state():
    return await env.state()