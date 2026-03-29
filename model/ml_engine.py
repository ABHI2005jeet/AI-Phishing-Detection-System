import joblib # type: ignore

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

THRESHOLD = 0.55

def ml_score(text):
    text_vec = vectorizer.transform([text])
    prob = model.predict_proba(text_vec)[0][1]

    score = round(prob * 100, 2)

    if prob >= THRESHOLD:
        label = "phishing"
    else:
        label = "legitimate"

    return label, score