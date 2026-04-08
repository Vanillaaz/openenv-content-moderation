from fastapi import FastAPI
from pydantic import BaseModel

from environment import ModerationEnv
from models import Action

app = FastAPI()
env = ModerationEnv()


# ----------- REQUEST MODEL -----------

class StepRequest(BaseModel):
    action: str


# ----------- ENDPOINTS -----------

# 🔥 RESET (NO BODY — IMPORTANT)
@app.post("/reset")
async def reset():
    result = await env.reset("easy")

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }


# 🔥 STEP
@app.post("/step")
async def step(req: StepRequest):
    result = await env.step(Action(action=req.action))

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }


# 🔥 STATE
@app.get("/state")
async def state():
    return await env.state()