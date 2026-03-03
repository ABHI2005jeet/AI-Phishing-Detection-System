import joblib
import numpy as np

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Adjustable threshold (upgrade 5)
THRESHOLD = 0.55  

def ml_score(text):
    text_vec = vectorizer.transform([text])
    prob = model.predict_proba(text_vec)[0][1]

    # Apply threshold tuning
    if prob >= THRESHOLD:
        return round(prob * 100, 2)
    else:
        return round(prob * 100, 2)