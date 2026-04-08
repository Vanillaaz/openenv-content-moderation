import asyncio
import os
from typing import List, Optional

from openai import OpenAI

from environment import ModerationEnv
from models import Action

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
TASK_NAME = os.getenv("MODERATION_TASK", "easy")
BENCHMARK = "content-moderation"
MAX_STEPS = 1  # Your env is single-step (done=True after first step)


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


def get_moderation_decision(client: OpenAI, content: str, task: str) -> str:
    system_prompt = """You are a content moderation AI. 
Your job is to classify content and decide whether to APPROVE or REMOVE it.
Reply with ONLY one of these exact words: APPROVE or REMOVE
- APPROVE: content is safe and acceptable
- REMOVE: content is harmful, toxic, hateful, or violates policies"""

    user_prompt = f"""Task difficulty: {task}
Content to moderate: {content}

Decision (APPROVE or REMOVE):"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=10,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip().upper()
        if "REMOVE" in text:
            return "REMOVE"
        return "APPROVE"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "APPROVE"


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = ModerationEnv()

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset(TASK_NAME)
        obs = result.observation

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            decision = get_moderation_decision(client, obs.content, obs.task)

            result = await env.step(Action(action=decision))

            reward = result.reward or 0.0
            done = result.done
            error = None

            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=decision, reward=reward, done=done, error=error)

            if done:
                break

        score = sum(rewards) / max(len(rewards), 1)
        score = min(max(score, 0.0), 1.0)
        success = score > 0.0

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)

    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())