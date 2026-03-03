from flask import Flask, render_template, request # type: ignore
import re

from model.ml_engine import ml_score
from engine.rule_engine import rule_score
from engine.url_engine import url_score

app = Flask(__name__)

scan_history = []

HIGHLIGHT_WORDS = [
    "verify", "account", "suspended", "bank",
    "login", "password", "otp", "urgent",
    "update", "security", "confirm"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/comparison")
def comparison():
    return render_template("comparison.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form.get("text", "")
    scan_type = request.form.get("scan_type", "text")

    # ML Score
    ml_s = ml_score(text)

    # Rule Score
    rule_s, rule_reasons = rule_score(text)

    # URL Score
    url_s, url_reasons = url_score(text)

    # Hybrid scoring
    if scan_type == "url":
        final_s = (url_s * 0.6) + (rule_s * 0.2) + (ml_s * 0.2)
    else:
        final_s = (ml_s * 0.6) + (rule_s * 0.25) + (url_s * 0.15)

    final_s = round(final_s, 2)

    # Category
    if final_s < 30:
        category = "Safe"
    elif final_s < 60:
        category = "Suspicious"
    else:
        category = "Phishing"

    # Threat Intelligence Simulation
    threat_flags = []

    if "192." in text or "http://" in text:
        threat_flags.append("Suspicious URL structure detected")

    if "bit.ly" in text or "tinyurl" in text:
        threat_flags.append("Shortened URL detected")

    if final_s > 70:
        threat_flags.append("High Risk Score — Possible blacklist match")

    # Combine reasons
    reasons = rule_reasons + url_reasons

    # Highlight suspicious words
    highlighted_text = text

    for word in HIGHLIGHT_WORDS:
        pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)
        highlighted_text = pattern.sub(
            f"<mark style='background-color:#ff4d4d;color:white;padding:3px 6px;border-radius:4px;'>{word}</mark>",
            highlighted_text
        )

    # Store history
    scan_history.append({
        "text": text[:50],
        "score": final_s,
        "category": category
    })

    return render_template(
        "result.html",
        ml_score=ml_s,
        rule_score=rule_s,
        url_score=url_s,
        final_score=final_s,
        category=category,
        reasons=reasons,
        threat_flags=threat_flags,
        highlighted_text=highlighted_text
    )


@app.route("/dashboard")
def dashboard():

    safe = sum(1 for s in scan_history if s["category"] == "Safe")
    suspicious = sum(1 for s in scan_history if s["category"] == "Suspicious")
    phishing = sum(1 for s in scan_history if s["category"] == "Phishing")

    return render_template(
        "dashboard.html",
        safe=safe,
        suspicious=suspicious,
        phishing=phishing,
        history=scan_history[::-1]
    )


@app.route("/metrics")
def metrics():
    return render_template("metrics.html")


if __name__ == "__main__":
    app.run(debug=True)