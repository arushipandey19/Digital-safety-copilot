import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

# =======================================================================
# STEP 1 — Load base CloveAI dataset
# =======================================================================
print("Loading CloveAI dataset...")
ds = load_dataset("CloveAI/india-spam-sms")
clove_df = ds["train"].to_pandas()[["text", "label"]]
print(f"CloveAI: {len(clove_df)} rows")

# =======================================================================
# STEP 2 — Fold in the 40 hand-written messages (test_messages_batch1.csv)
# Already used once for evaluation - now moving into training since the
# team's real hand-written set will become the new holdout.
# =======================================================================
batch1_df = pd.read_csv("test_messages_batch1.csv")[["text", "expected_label"]]
batch1_df = batch1_df.rename(columns={"expected_label": "label"})
print(f"test_messages_batch1.csv: {len(batch1_df)} rows")

# =======================================================================
# STEP 3 — Fold in the 100-row AI-generated dataset
# (digital_safety_message_dataset_100.csv) - useful for volume and
# category coverage, but AI-authored, so training-only, never testing.
# =======================================================================
ai100_df = pd.read_csv("digital_safety_message_dataset_100.csv")
ai100_df = ai100_df.rename(columns={"message": "text"})[["text", "label"]]
print(f"digital_safety_message_dataset_100.csv: {len(ai100_df)} rows")

# =======================================================================
# STEP 4 — Combine all training sources
# =======================================================================
df = pd.concat([clove_df, batch1_df, ai100_df], ignore_index=True)
df = df.drop_duplicates(subset="text").reset_index(drop=True)
print(f"\nCombined training set: {len(df)} rows")
print(df["label"].value_counts())

df.to_csv("combined_training_data.csv", index=False)
print("Saved combined_training_data.csv")

# =======================================================================
# STEP 5 — Split, vectorize, train
# =======================================================================
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train = vectorizer.fit_transform(train_df["text"])
X_test = vectorizer.transform(test_df["text"])

model = MultinomialNB()
model.fit(X_train, train_df["label"])

# =======================================================================
# STEP 6 — Synthetic split performance (still not the trustworthy number)
# =======================================================================
preds = model.predict(X_test)
print("\n=== Synthetic test-split performance (not the real generalization number) ===")
print(classification_report(test_df["label"], preds))

# Save for backend
joblib.dump(model, "ml_classifier.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Saved model + vectorizer.")

# =======================================================================
# STEP 7 — Evaluate on the team's REAL hand-written holdout, once it exists
# Save the team's hand-typed file as team_holdout.csv in this folder,
# with columns: text, label (or expected_label), category
# =======================================================================
try:
    holdout_df = pd.read_csv("real_documented_scams.csv")
    if "expected_label" in holdout_df.columns:
        holdout_df = holdout_df.rename(columns={"expected_label": "label"})
    if "message" in holdout_df.columns and "text" not in holdout_df.columns:
        holdout_df = holdout_df.rename(columns={"message": "text"})

    X_holdout = vectorizer.transform(holdout_df["text"])
    holdout_preds = model.predict(X_holdout)
    holdout_probs = model.predict_proba(X_holdout)

    print("\n=== TEAM HOLDOUT performance (real_documented_scams.csv) — this is your real number ===")
    for _, row in holdout_df.assign(pred=holdout_preds, conf=holdout_probs.max(axis=1)).iterrows():
        mark = "OK " if row["pred"] == row["label"] else "MISS"
        cat = row["category"] if "category" in holdout_df.columns else ""
        print(f"[{mark}] expected={row['label']} predicted={row['pred']} "
              f"(conf {row['conf']:.2f}) [{cat}] {row['text'][:60]}")

    print("\n" + classification_report(holdout_df["label"], holdout_preds))

except FileNotFoundError:
    print("\n(real_documented_scams.csv not found yet — waiting on the team's genuinely "
          "hand-written messages. Add it to this folder once ready, then rerun.)")

# =======================================================================
# STEP 8 — Quick manual sanity check
# =======================================================================
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

print("\n=== Manual sanity check ===")
for msg, pred, prob in zip(test_messages, preds, probs):
    print(f"{pred} (conf: {prob.max():.2f}) — {msg}")