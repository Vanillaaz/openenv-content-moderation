from fastapi import FastAPI
from pydantic import BaseModel
from environment import ModerationEnv
from models import Action

app = FastAPI()

env = ModerationEnv()


# ----------- REQUEST MODELS -----------

class StepRequest(BaseModel):
    action: str


# ----------- ENDPOINTS -----------

# ✅ FIXED RESET (no body required)
@app.post("/reset")
async def reset():
    result = await env.reset()

    return {
        "observation": result.observation.dict(),  # ✅ revert this
        "reward": result.reward,
        "done": result.done
    }


# ✅ STEP endpoint
@app.post("/step")
async def step(req: StepRequest):
    action = Action(action=req.action)
    result = await env.step(action)

    return {
        "observation": result.observation.dict(),  # ✅ same here
        "reward": result.reward,
        "done": result.done
    }


# ✅ STATE endpoint
@app.get("/state")
async def state():
    return await env.state()