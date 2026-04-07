from fastapi import FastAPI
from pydantic import BaseModel
from environment import ModerationEnv
from models import Action

app = FastAPI()

env = ModerationEnv()

class ResetRequest(BaseModel):
    task: str = "easy"

class StepRequest(BaseModel):
    action: str

@app.post("/reset")
async def reset(req: ResetRequest):
    result = await env.reset(req.task)
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