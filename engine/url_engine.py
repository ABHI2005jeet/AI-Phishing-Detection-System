import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "login","verify","secure","account",
    "update","bank","paypal","password"
]

def url_score(text):

    score = 0
    reasons = []

    url = text.lower().strip()

    # 1️⃣ URL length
    if len(url) > 75:
        score += 10
        reasons.append("Unusually long URL detected")

    # 2️⃣ Too many dots
    if url.count(".") > 3:
        score += 15
        reasons.append("Too many subdomains detected")

    # 3️⃣ Hyphen in domain
    if "-" in url:
        score += 10
        reasons.append("Suspicious hyphenated domain")

    # 4️⃣ IP address instead of domain
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 25
        reasons.append("IP-based URL detected")

    # 5️⃣ HTTP instead of HTTPS
    if url.startswith("http://"):
        score += 10
        reasons.append("URL not using HTTPS")

    # 6️⃣ Suspicious keywords
    for word in SUSPICIOUS_KEYWORDS:
        if word in url:
            score += 5
            reasons.append(f"Suspicious keyword in URL: {word}")

    # 7️⃣ @ symbol
    if "@" in url:
        score += 10
        reasons.append("URL contains @ symbol")

    # 8️⃣ Excessive numbers
    if len(re.findall(r"\d", url)) > 5:
        score += 10
        reasons.append("Too many numbers in URL")

    # 9️⃣ URL path depth
    parsed = urlparse(url)
    path_depth = parsed.path.count("/")

    if path_depth > 5:
        score += 10
        reasons.append("Deep URL path structure detected")

    # 10️⃣ Suspicious file types
    if re.search(r"\.(exe|zip|scr|rar|doc|xls)", url):
        score += 15
        reasons.append("Suspicious file download detected")

    score = min(score,100)

    return score, reasons