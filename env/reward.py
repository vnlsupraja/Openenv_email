# env/reward.py


def compute_reward(action, expected_step):
    if not expected_step:
        return -0.5, "invalid email"

    if action["type"] != expected_step["type"]:
        return -0.3, "wrong step"

    if "content" in expected_step:
        if expected_step["content"].lower() in action.get("content", "").lower():
            return 1.0, "perfect response"
        return 0.5, "partial response"

    return 0.8, "correct step"