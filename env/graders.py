# env/graders.py

def grade(history, expected_map):
    """
    Grade the sequence of actions against expected actions.
    
    Args:
        history: List of action dicts with (email_id, type, content)
        expected_map: Dict mapping email_id to list of expected action dicts
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Hackathon validator expects score to be strictly in (0, 1).
    # Keep a tiny margin from the boundaries for all outcomes.
    eps = 0.001

    if not expected_map or not history:
        return eps
    
    total_steps = 0
    correct_steps = 0
    progress = {k: 0 for k in expected_map}

    for action in history:
        eid = action.get("email_id")

        if eid not in expected_map:
            continue

        expected_steps = expected_map[eid]
        idx = progress.get(eid, 0)

        if idx >= len(expected_steps):
            continue

        expected = expected_steps[idx]
        total_steps += 1

        if action.get("type") == expected.get("type"):
            if "content" in expected:
                if expected["content"].lower() in action.get("content", "").lower():
                    correct_steps += 1
            else:
                correct_steps += 1

            progress[eid] = idx + 1

    raw_score = (correct_steps / total_steps) if total_steps > 0 else 0.0
    return max(eps, min(1.0 - eps, raw_score))


