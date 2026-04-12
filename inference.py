import asyncio
import os
from typing import List, Optional

from openai import OpenAI

from environment import ModerationEnv
from models import Action

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
BENCHMARK = "content-moderation"
MAX_STEPS = 1
TASKS = ["easy", "medium", "hard", "expert"]


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
Classify the given content and respond in EXACTLY this format (no extra text):
label=<label>;decision=<decision>;severity=<severity>

For label use one of: safe, toxic, hate, spam
For decision use one of: approve, warn, remove
For severity use one of: none, low, medium, high

Examples:
label=safe;decision=approve;severity=none
label=toxic;decision=warn;severity=medium
label=hate;decision=remove;severity=high"""

    user_prompt = f"""Task difficulty: {task}
Content to moderate: {content}

Respond with ONLY the classification line:"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=30,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        if "label=" in text and "=" in text:
            return text.split("\n")[0].strip()
        return "label=safe;decision=approve;severity=none"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "label=safe;decision=approve;severity=none"


async def run_task(task_name: str, client: OpenAI) -> None:
    env = ModerationEnv()
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset(task_name)
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
        score = min(max(score, 0.01), 0.98)
        success = score > 0.01

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)

    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    for task_name in TASKS:
        await run_task(task_name, client)


if __name__ == "__main__":
    asyncio.run(main())