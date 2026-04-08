def grade(task_data, action_str):
    try:
        parts = dict(item.split("=") for item in action_str.split(";"))
    except:
        return 0.01  # never return exact 0.0

    reward = 0.0

    # LABEL MATCH
    if parts.get("label") == task_data.get("label"):
        reward += 0.5

    # DECISION MATCH (for hard tasks)
    if "decision" in task_data:
        if parts.get("decision") == task_data.get("decision"):
            reward += 0.29  # 0.5 + 0.29 = 0.79 (not 1.0)

    # SEVERITY MATCH (optional)
    if "severity" in task_data:
        if parts.get("severity") == task_data.get("severity"):
            reward += 0.19  # 0.5 + 0.29 + 0.19 = 0.98 (not 1.0)

    # Clamp to strictly (0, 1) - never exactly 0.0 or 1.0
    reward = max(0.01, min(reward, 0.98))

    return reward