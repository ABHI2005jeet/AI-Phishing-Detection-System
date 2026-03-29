import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from url_features import extract_features

# load dataset
df = pd.read_csv("data/url_dataset_final.csv")

print("Dataset size:", len(df))

# feature extraction
X = df["url"].apply(extract_features).tolist()
y = df["label"]

# split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = RandomForestClassifier(n_estimators=200)

model.fit(X_train, y_train)

# evaluate
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("URL Model Accuracy:", accuracy)

# save model
joblib.dump(model, "model/url_model.pkl")

print("URL model saved → model/url_model.pkl")