TASKS = {
    "easy": [
        {"content": "I love this product!", "label": "safe", "decision": "approve", "severity": "none"},
        {"content": "You are stupid and ugly", "label": "toxic", "decision": "warn", "severity": "low"},
        {"content": "The weather is nice today", "label": "safe", "decision": "approve", "severity": "none"},
        {"content": "I hate you so much", "label": "toxic", "decision": "warn", "severity": "medium"},
    ],

    "medium": [
        {"content": "Go back to your country", "label": "hate", "decision": "remove", "severity": "high"},
        {"content": "Buy now!!! Limited offer!!!", "label": "spam", "decision": "remove", "severity": "low"},
        {"content": "People like you don't belong here", "label": "hate", "decision": "remove", "severity": "high"},
        {"content": "CLICK HERE TO WIN $1000 FREE!!!!", "label": "spam", "decision": "remove", "severity": "medium"},
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
        },
        {
            "content": "Your kind has always been inferior",
            "label": "hate",
            "decision": "remove",
            "severity": "high"
        },
        {
            "content": "Maybe you should just disappear forever",
            "label": "toxic",
            "decision": "warn",
            "severity": "medium"
        },
    ],

    "expert": [
        {
            "content": "I'm not racist but those people are just naturally less intelligent",
            "label": "hate",
            "decision": "remove",
            "severity": "high"
        },
        {
            "content": "You're not completely worthless, you could be used as a bad example",
            "label": "toxic",
            "decision": "warn",
            "severity": "low"
        },
        {
            "content": "This is totally fine content with no issues whatsoever",
            "label": "safe",
            "decision": "approve",
            "severity": "none"
        },
    ]
}