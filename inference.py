import asyncio
import os
from typing import List, Optional
from openai import OpenAI

from environment import ModerationEnv
from models import Action

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

MAX_STEPS = 3

SYSTEM_PROMPT = """
You are a content moderation agent.

Given text, respond ONLY in this format:
label=<label>;decision=<decision>;severity=<severity>

Labels: safe, toxic, hate, spam
Decision: allow, warn, remove
Severity: low, medium, high

Do not add anything else.
"""

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_model_action(client, content):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            temperature=0.3,
            max_tokens=50,
        )
        return completion.choices[0].message.content.strip()
    except:
        return "label=safe;decision=allow;severity=low"

async def run_task(task_name):
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = ModerationEnv()

    rewards = []
    steps_taken = 0

    log_start(task=task_name, env="moderation_env", model=MODEL_NAME)

    result = await env.reset(task_name)
    content = result.observation.content

    for step in range(1, MAX_STEPS + 1):
        action_str = get_model_action(client, content)

        result = await env.step(Action(action=action_str))

        reward = result.reward
        done = result.done

        rewards.append(reward)
        steps_taken = step

        log_step(step, action_str, reward, done, None)

        if done:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = score > 0.5

    await env.close()
    log_end(success, steps_taken, score, rewards)

async def main():
    for task in ["easy", "medium", "hard"]:
        await run_task(task)

if __name__ == "__main__":
    asyncio.run(main())