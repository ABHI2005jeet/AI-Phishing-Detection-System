import pandas as pd # type: ignore
import numpy as np# type: ignore
import joblib# type: ignore

from sklearn.model_selection import train_test_split# type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer# type: ignore
from sklearn.linear_model import LogisticRegression# type: ignore
from sklearn.calibration import CalibratedClassifierCV# type: ignore
from sklearn.metrics import classification_report, confusion_matrix# type: ignore

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/email_dataset.csv")

print("Columns:", df.columns)

# Make sure correct columns exist
# Adjust if needed
df = df[['text', 'label']]

df = df.dropna()

print("Original Distribution:\n", df.label.value_counts())

# =========================
# BALANCE DATASET
# =========================

phish = df[df.label == 1]
clean = df[df.label == 0]

# Downsample phishing if too large
if len(phish) > len(clean) * 2:
    phish = phish.sample(n=len(clean) * 2, random_state=42)

df_balanced = pd.concat([phish, clean])
df_balanced = df_balanced.sample(frac=1, random_state=42)

print("Balanced Distribution:\n", df_balanced.label.value_counts())

# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    df_balanced.text,
    df_balanced.label,
    test_size=0.2,
    random_state=42,
    stratify=df_balanced.label
)

# =========================
# TFIDF
# =========================

vectorizer = TfidfVectorizer(
    max_features=8000,
    ngram_range=(1,2),
    stop_words='english'
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =========================
# MODEL
# =========================

base_model = LogisticRegression(
    class_weight="balanced",
    max_iter=300
)

model = CalibratedClassifierCV(base_model, method='sigmoid')
model.fit(X_train_vec, y_train)

# =========================
# EVALUATION
# =========================

y_pred = model.predict(X_test_vec)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================
# SAVE
# =========================

joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\nModel Saved Successfully")