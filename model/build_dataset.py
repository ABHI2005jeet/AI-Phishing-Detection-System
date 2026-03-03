import pandas as pd
import os

# ===============================
# PATHS (Adjust if needed)
# ===============================

base_phishing = r"C:\Users\Abhij\.cache\kagglehub\datasets\naserabdullahalam\phishing-email-dataset\versions\1"
base_spam = r"C:\Users\Abhij\.cache\kagglehub\datasets\uciml\sms-spam-collection-dataset\versions\1"
base_enron = r"C:\Users\Abhij\.cache\kagglehub\datasets\wcukierski\enron-email-dataset\versions\1"

dataframes = []

# ===============================
# LOAD PHISHING EMAILS
# ===============================
phish_path = os.path.join(base_phishing, "phishing_email.csv")
phish_df = pd.read_csv(phish_path, encoding="latin1")
phish_df = phish_df.iloc[:, 0:1]
phish_df.columns = ["text"]
phish_df["label"] = 1
dataframes.append(phish_df)

# ===============================
# LOAD SMS SPAM DATASET
# ===============================
spam_path = os.path.join(base_spam, "spam.csv")
spam_df = pd.read_csv(spam_path, encoding="latin1")
spam_df = spam_df.iloc[:, 0:2]
spam_df.columns = ["label_text", "text"]
spam_df["label"] = spam_df["label_text"].map({"ham": 0, "spam": 1})
spam_df = spam_df[["text", "label"]]
dataframes.append(spam_df)

# ===============================
# LOAD ENRON LEGIT EMAILS
# ===============================
import glob

enron_files = glob.glob(base_enron + "/**/*.txt", recursive=True)

legit_texts = []
for file in enron_files[:15000]:  # limit to avoid overload
    try:
        with open(file, "r", encoding="latin1") as f:
            legit_texts.append(f.read())
    except:
        continue

enron_df = pd.DataFrame({
    "text": legit_texts,
    "label": 0
})

dataframes.append(enron_df)

# ===============================
# COMBINE
# ===============================
big_df = pd.concat(dataframes, ignore_index=True)

big_df = big_df.dropna()
big_df["text"] = big_df["text"].astype(str)

print("Final Dataset Size:", len(big_df))
print(big_df["label"].value_counts())

os.makedirs("data", exist_ok=True)
big_df.to_csv("data/combined_dataset.csv", index=False)

print("Dataset Created Successfully")