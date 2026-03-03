import re

def url_score(text):

    score = 0
    reasons = []

    text_lower = text.lower()

    if text_lower.count('.') > 3:
        score += 20
        reasons.append("Too many subdomains detected")

    if "-" in text_lower:
        score += 10
        reasons.append("Suspicious hyphenated domain")

    if re.search(r"\d+\.\d+\.\d+\.\d+", text_lower):
        score += 25
        reasons.append("IP-based URL detected")

    score = min(score, 100)

    return score, reasons