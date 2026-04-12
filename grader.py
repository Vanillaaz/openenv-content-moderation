def grade(task_data, action_str):
    try:
        parts = dict(item.split("=") for item in action_str.split(";"))
    except:
        return 0.01

    reward = 0.0

    if parts.get("label") == task_data.get("label"):
        reward += 0.5

    if "decision" in task_data:
        if parts.get("decision") == task_data.get("decision"):
            reward += 0.29

    if "severity" in task_data:
        if parts.get("severity") == task_data.get("severity"):
            reward += 0.19

    reward = max(0.01, min(reward, 0.98))

    return reward