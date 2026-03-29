import re
from urllib.parse import urlparse

def extract_features(url):

    url = str(url).lower()

    features = {}

    features["url_length"] = len(url)
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["digit_count"] = len(re.findall(r"\d", url))
    features["has_https"] = int(url.startswith("https"))
    features["has_http"] = int(url.startswith("http"))
    features["has_ip"] = int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url)))
    features["has_at"] = int("@" in url)

    parsed = urlparse(url)

    features["path_length"] = len(parsed.path)
    features["path_depth"] = parsed.path.count("/")

    suspicious_words = [
        "login","verify","secure","account",
        "update","bank","paypal","password"
    ]

    features["keyword_count"] = sum(word in url for word in suspicious_words)

    return list(features.values())