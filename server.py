from fastapi import FastAPI, Request
from pydantic import BaseModel

from environment import ModerationEnv
from models import Action

app = FastAPI()
env = ModerationEnv()


# ----------- REQUEST MODEL -----------

class StepRequest(BaseModel):
    action: str


# ----------- ENDPOINTS -----------

@app.post("/reset")
async def reset(request: Request):
    task = "easy"

    if request.headers.get("content-type") == "application/json":
        try:
            body = await request.json()
            if isinstance(body, dict):
                task = body.get("task", "easy")
        except:
            pass

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