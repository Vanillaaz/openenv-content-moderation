def grade(task_data, action_str):
    try:
        parts = dict(item.split("=") for item in action_str.split(";"))
    except:
        return 0.0

    reward = 0.0

    # LABEL MATCH
    if parts.get("label") == task_data.get("label"):
        reward += 0.5

    # DECISION MATCH (for hard tasks)
    if "decision" in task_data:
        if parts.get("decision") == task_data.get("decision"):
            reward += 0.3

    # SEVERITY MATCH (optional)
    if "severity" in task_data:
        if parts.get("severity") == task_data.get("severity"):
            reward += 0.2

    return reward