# Sentinel AI – Hybrid Phishing Detection System

An intelligent **AI-based phishing detection platform** that identifies malicious **emails, messages, and URLs** using a combination of **Machine Learning, rule-based detection, and threat intelligence**.

The system provides **real-time scanning, explainable risk signals, analytics dashboard, and downloadable PDF reports**, helping users identify phishing attempts quickly and effectively.

---

# Features

• AI-powered **Email Phishing Detection**
• **URL Phishing Detection** using machine learning
• **Rule-based phishing detection engine**
• **Structural URL feature analysis**
• **Hybrid threat scoring model**
• **Explainable AI risk signals**
• **Threat Intelligence integration (PhishTank)**
• **Interactive web scanning interface**
• **Detection analytics dashboard**
• **Scan history tracking**
• **Automated PDF scan report generation**

---

# System Architecture

User Input (Email / URL)
↓
Flask Web Application
↓
Detection Engines

• Email ML Model (Logistic Regression + TF-IDF)
• URL ML Model (Random Forest + Feature Extraction)
• Rule-Based Detection Engine
• URL Structural Feature Analyzer
• Threat Intelligence Lookup

↓

Hybrid Scoring System
↓
Detection Result (Safe / Suspicious / Phishing)
↓
Dashboard + PDF Report

---

# Machine Learning Models

## Email Phishing Detection

Algorithm:

Logistic Regression

Text Processing:

TF-IDF Vectorization

Dataset:

Email phishing dataset

Performance:

Accuracy ≈ **98%**

---

## URL Phishing Detection

Algorithm:

Random Forest Classifier

Feature Extraction Includes:

• URL length
• Number of dots
• Hyphen count
• Digit count
• Path depth
• HTTPS usage
• Suspicious keywords
• IP address detection

Dataset size:

Over **500,000 URLs**

Performance:

Accuracy ≈ **89%**

---

# Explainable AI Signals

Instead of only showing predictions, the system explains **why a URL or message was flagged**.

Example signals:

• Suspicious domain extension
• Multiple hyphens in domain
• High-risk keywords detected
• HTTP instead of HTTPS
• Suspicious URL structure

---

# Tech Stack

Backend
• Python
• Flask

Machine Learning
• Scikit-learn
• Pandas
• NumPy

Frontend
• HTML
• CSS
• Bootstrap

Visualization
• Chart.js

Threat Intelligence
• PhishTank API

Reporting
• ReportLab (PDF generation)

---

# Project Structure

AI-Phishing-Detection-System

app.py
engine/
 rule_engine.py
 url_engine.py
 threat_intel.py

model/
 ml_engine.py
 url_ml_engine.py
 url_features.py
 train.py
 train_url_model.py

templates/
static/

README.md
requirements.txt

---

# How to Clone This Repository

Copy the repository URL and run:

```
git clone https://github.com/ABHI2005jeet/AI-Phishing-Detection-System.git
```

Move into the project folder:

```
cd AI-Phishing-Detection-System
```

---

# How to Fork This Repository

Click the **Fork** button at the top of this page.

Then clone your fork:

```
git clone https://github.com/YOUR-USERNAME/AI-Phishing-Detection-System.git
```

---

# How to Run the Project

### 1. Create Virtual Environment

```
python -m venv venv
```

### 2. Activate Virtual Environment

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Run the Application

```
python app.py
```

Open the browser:

```
http://127.0.0.1:5000
```

---

# Datasets

Datasets are not included in this repository due to **GitHub file size limitations**.

The models were trained using:

• Email phishing dataset
• Phishing URL dataset
• Safe domain dataset

Place datasets inside:

```
data/
```

before training the models.

---

# Research Inspiration

This project draws inspiration from academic research including:

**An Intelligent Phishing Email Detection System Using Ensemble Methods and Explainable AI**

and other studies on **machine learning based phishing website detection**.

---

# Future Improvements

Potential upgrades for production-level deployment:

• Deep learning models (BERT / Transformers)
• Browser extension for real-time phishing detection
• Domain reputation analysis using WHOIS and DNS
• Integration with OpenPhish / VirusTotal feeds
• SOC-style real-time monitoring dashboard
• Email file scanning (.eml analysis)

---

# Author

Abhijeet Kumar
BTech Cyber Security

