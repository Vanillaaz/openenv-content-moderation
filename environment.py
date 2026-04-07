import random
from models import Observation, StepResult
from tasks import TASKS
from grader import grade

class ModerationEnv:

    def __init__(self):
        self.current_task = None
        self.current_data = None
        self.done = False

    async def reset(self, task="easy"):
        self.current_task = task
        self.current_data = random.choice(TASKS[task])
        self.done = False

        return StepResult(
            observation=Observation(
                content=self.current_data["content"],
                task=task
            ),
            reward=0.0,
            done=False,
            info={}
        )

    async def step(self, action):
        # 🚨 FIX: never return observation=None
        if self.done:
            return StepResult(
                observation=Observation(
                    content=self.current_data["content"],
                    task=self.current_task
                ),
                reward=0.0,
                done=True,
                info={"message": "Episode already finished"}
            )

        reward = grade(self.current_data, action.action)
        self.done = True

        return StepResult(
            observation=Observation(
                content=self.current_data["content"],
                task=self.current_task
            ),
            reward=reward,
            done=True,
            info={}
        )

    async def state(self):
        return {
            "task": self.current_task,
            "data": self.current_data
        }

    async def close(self):
        pass