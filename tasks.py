TASKS = {
    "easy": [
        {"content": "I love this product!", "label": "safe"},
        {"content": "You are stupid", "label": "toxic"}
    ],

    "medium": [
        {"content": "Go back to your country", "label": "hate"},
        {"content": "Buy now!!! Limited offer!!!", "label": "spam"}
    ],

    "hard": [
        {
            "content": "Wow you're such a genius 🤡",
            "label": "toxic",
            "decision": "warn",
            "severity": "medium"
        },
        {
            "content": "I will find you and hurt you",
            "label": "toxic",
            "decision": "remove",
            "severity": "high"
        }
    ]
}