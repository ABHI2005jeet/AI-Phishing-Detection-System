from flask import Flask, render_template, request # type: ignore
from model.url_ml_engine import url_ml_score
from engine.threat_intel import check_phishtank
from reportlab.lib.pagesizes import letter# type: ignore
from reportlab.pdfgen import canvas# type: ignore
from datetime import datetime
from flask import send_file# type: ignore
import os
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

def generate_pdf_report(input_text, score, category, reasons):

    file_path = "scan_report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    c.setFont("Helvetica", 12)

    y = 750

    c.drawString(50, y, "Sentinel AI - Phishing Detection Report")
    y -= 30

    c.drawString(50, y, f"Scan Time: {datetime.now()}")
    y -= 30

    c.drawString(50, y, f"Input Scanned:")
    y -= 20

    c.drawString(50, y, input_text[:100])
    y -= 40

    c.drawString(50, y, f"Threat Score: {score}%")
    y -= 20

    c.drawString(50, y, f"Category: {category}")
    y -= 30

    c.drawString(50, y, "Detected Risk Signals:")
    y -= 20

    for r in reasons:
        c.drawString(60, y, f"- {r}")
        y -= 20

    c.save()

    return file_path

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download_report")
def download_report():
    return send_file("scan_report.pdf", as_attachment=True)

@app.route("/comparison")
def comparison():
    return render_template("comparison.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form.get("text", "")
    scan_type = request.form.get("scan_type", "text")

    # URL ML score (new model)
    url_ml_s, url_ml_explain = url_ml_score(text)

    # Email ML score
    ml_label, ml_s = ml_score(text)

    # Rule engine
    rule_s, rule_reasons = rule_score(text)

    # URL feature engine
    url_s, url_reasons = url_score(text)
    
   # Threat flags list
    threat_flags = []

# Threat intelligence check (only for URLs)
    if scan_type == "url" and check_phishtank(text):
        threat_flags.append("Known phishing URL detected via threat intelligence database")
        url_s += 40

# Hybrid scoring
    if scan_type == "url":
        final_s = (url_ml_s * 0.4) + (url_s * 0.4) + (rule_s * 0.2)
    else:
        final_s = (ml_s * 0.6) + (rule_s * 0.25) + (url_s * 0.15)

    final_s = round(final_s, 2)
    # Category
    if final_s < 35:
        category = "Safe"
    elif final_s < 65:
        category = "Suspicious"
    else:
        category = "Phishing"
    

    if "192." in text or "http://" in text:
        threat_flags.append("Suspicious URL structure detected")

    if "bit.ly" in text or "tinyurl" in text:
        threat_flags.append("Shortened URL detected")

    if final_s > 70:
        threat_flags.append("High Risk Score — Possible blacklist match")

    # Combine reasons
    reasons = sorted(set(rule_reasons + url_reasons + url_ml_explain))

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
    report_file = generate_pdf_report(text, final_s, category, reasons)

    return render_template(
        "result.html",
        ml_score=ml_s,
        url_ml_score=url_ml_s,
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