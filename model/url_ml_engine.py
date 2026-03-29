import joblib# type: ignore
from model.url_features import extract_features

model = joblib.load("model/url_model.pkl")

FEATURE_NAMES = [
    "url_length",
    "dot_count",
    "hyphen_count",
    "digit_count",
    "has_https",
    "has_http",
    "has_ip",
    "has_at",
    "path_length",
    "path_depth",
    "keyword_count"
]


def url_ml_score(url):

    features = extract_features(url)

    prob = model.predict_proba([features])[0][1]

    explanations = []

    # unpack features
    url_length, dot_count, hyphen_count, digit_count, https, http, ip, at, path_len, path_depth, keyword_count = features

    if url_length > 75:
        explanations.append("Unusually long URL detected")

    if dot_count > 3:
        explanations.append("Too many subdomains detected")

    if hyphen_count > 2:
        explanations.append("Multiple hyphens in domain")

    if digit_count > 5:
        explanations.append("Too many numbers in URL")

    if http == 1 and https == 0:
        explanations.append("URL not using HTTPS")

    if ip == 1:
        explanations.append("IP address used instead of domain")

    if at == 1:
        explanations.append("URL contains @ symbol")

    if path_depth > 5:
        explanations.append("Deep URL path structure")

    if keyword_count > 0:
        explanations.append("Suspicious keywords detected in URL")

    return round(prob * 100, 2), explanations