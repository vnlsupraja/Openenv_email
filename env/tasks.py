# env/tasks.py
import json

class EasyTask:
    """Spam classification"""

    def __init__(self):
        with open("data/emails.json") as f:
            self.dataset = json.load(f)

    def get_initial_state(self):
        return {
            "inbox": self.dataset[:2]
        }

    def get_expected_actions(self):
        return {e["id"]: e["expected_actions"] for e in self.dataset[:2]}

    def is_done(self, state, history):
        return len(history) >= 2


class MediumTask:
    """Prioritization + classification"""

    def __init__(self):
        with open("data/emails.json") as f:
            self.dataset = json.load(f)

    def get_initial_state(self):
        return {
            "inbox": self.dataset[2:6]
        }

    def get_expected_actions(self):
        return {e["id"]: e["expected_actions"] for e in self.dataset[2:6]}

    def is_done(self, state, history):
        return len(history) >= 4


class HardTask:
    """Full workflow"""

    def __init__(self):
        with open("data/emails.json") as f:
            self.dataset = json.load(f)

    def get_initial_state(self):
        return {
            "inbox": self.dataset[6:12]
        }

    def get_expected_actions(self):
        return {e["id"]: e["expected_actions"] for e in self.dataset[6:12]}

    def is_done(self, state, history):
        return len(history) >= 6