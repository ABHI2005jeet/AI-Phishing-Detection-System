import re

HIGH_RISK_WORDS = [
    "verify", "account", "suspended", "bank",
    "login", "password", "otp", "urgent",
    "update", "security", "confirm"
]

SUSPICIOUS_TLDS = ["xyz", "top", "club", "work", "info"]
SHORTENERS = ["bit.ly", "tinyurl", "t.co", "goo.gl"]

def rule_score(text):

    score = 0
    reasons = []

    text_lower = text.lower()

    # Keyword detection
    for word in HIGH_RISK_WORDS:
        if word in text_lower:
            score += 10
            reasons.append(f"High-risk keyword detected: {word}")

    # HTTP detection
    if "http://" in text_lower:
        score += 15
        reasons.append("Unsecured HTTP link detected")

    # IP based link
    if re.search(r"\d+\.\d+\.\d+\.\d+", text_lower):
        score += 20
        reasons.append("IP address used instead of domain")

    # Suspicious domain extension
    for tld in SUSPICIOUS_TLDS:
        if f".{tld}" in text_lower:
            score += 10
            reasons.append(f"Suspicious domain extension detected: .{tld}")

    # URL shortener
    for short in SHORTENERS:
        if short in text_lower:
            score += 15
            reasons.append(f"URL shortener detected: {short}")

    # Too many numbers
    if len(re.findall(r"\d", text_lower)) > 5:
        score += 10
        reasons.append("Too many numbers detected in message/URL")

    score = min(score, 100)

    return score, reasons