from datasets import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load dataset
ds = load_dataset("CloveAI/india-spam-sms")
df = ds["train"].to_pandas()
print(df.head())
print(df["label"].value_counts())

# Split
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)

# Vectorize + train
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train = vectorizer.fit_transform(train_df["text"])
X_test = vectorizer.transform(test_df["text"])

model = LogisticRegression()
model.fit(X_train, train_df["label"])

# Evaluate
preds = model.predict(X_test)
print(classification_report(test_df["label"], preds))

# Save for backend
joblib.dump(model, "ml_classifier.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Saved model + vectorizer.")

test_messages = [
    "Dear customer your SBI account will be blocked today update KYC immediately click here",
    "Hey are we still on for lunch tomorrow?",
    "Congratulations you have won Rs 50000 lottery claim now by sharing OTP",
    "Your Amazon order has been shipped, track here",
    "URGENT: Your electricity connection will be cut in 2 hours, pay now to avoid disconnection",
]

test_vec = vectorizer.transform(test_messages)
preds = model.predict(test_vec)
probs = model.predict_proba(test_vec)

for msg, pred, prob in zip(test_messages, preds, probs):
    print(f"{pred} (conf: {prob.max():.2f}) — {msg}")