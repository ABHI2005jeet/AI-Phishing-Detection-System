import re

HIGH_RISK_WORDS = [
    "verify", "account", "suspended", "bank",
    "login", "password", "otp", "urgent",
    "update", "security", "confirm"
]

def rule_score(text):

    score = 0
    reasons = []

    text_lower = text.lower()

    for word in HIGH_RISK_WORDS:
        if word in text_lower:
            score += 10
            reasons.append(f"High-risk keyword detected: {word}")

    if "http://" in text_lower:
        score += 15
        reasons.append("Unsecured HTTP link detected")

    if re.search(r"\d+\.\d+\.\d+\.\d+", text_lower):
        score += 20
        reasons.append("IP address used instead of domain")

    score = min(score, 100)

    return score, reasons