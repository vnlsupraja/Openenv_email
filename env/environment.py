# env/environment.py
from .models import Observation, Action, Reward, Email
from .reward import compute_reward
from .graders import grade

class EmailEnv:
    def __init__(self, task):
        self.task = task
        self.state_data = None
        self.history = []
        self.progress = {}  # track per email step

    def reset(self):
        self.state_data = self.task.get_initial_state()
        self.history = []
        self.progress = {}

        emails = [Email(**e) for e in self.state_data["inbox"]]

        return Observation(inbox=emails, last_action_result=None)

    def state(self):
        return self.state_data

    def step(self, action: Action):
        eid = action.email_id
        idx = self.progress.get(eid, 0)

        expected_steps = self.task.get_expected_actions().get(eid, [])
        if idx < len(expected_steps):
            expected_step = expected_steps[idx]
            reward_value, reason = compute_reward(action.dict(), expected_step)
            if reward_value > 0:
                self.progress[eid] = idx + 1
        else:
            reward_value, reason = -0.5, "already completed or invalid"

        self.history.append(action.dict())

        done = self.task.is_done(self.state_data, self.history)

        obs = Observation(
            inbox=[Email(**e) for e in self.state_data["inbox"]],
            last_action_result=reason
        )

        reward = Reward(value=reward_value, reason=reason)

        info = {
            "score": grade(self.history, self.task.get_expected_actions())
        }

        return obs, reward, done, info