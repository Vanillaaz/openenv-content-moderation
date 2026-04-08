from environment import ModerationEnv
from models import Action

env = ModerationEnv()

async def reset():
    result = await env.reset()
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }

async def step(action: dict):
    act = Action(**action)
    result = await env.step(act)
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done
    }