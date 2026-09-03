"""
Compare multiple text classification models — trained on the same data,
evaluated on the REAL holdout (test_messages_batch1.csv), not the
misleading synthetic train/test split.

Usage:
    python compare_models.py
"""

from datasets import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ---- Load training data ----
print("Loading CloveAI dataset...")
ds = load_dataset("CloveAI/india-spam-sms")
df = ds["train"].to_pandas()

train_df, synth_test_df = train_test_split(
    df, test_size=0.2, stratify=df["label"], random_state=42
)

# ---- Load the REAL holdout ----
holdout_df = pd.read_csv("test_messages_batch1.csv")

# ---- Vectorize (same vectorizer used for all models, for fair comparison) ----
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train = vectorizer.fit_transform(train_df["text"])
X_synth_test = vectorizer.transform(synth_test_df["text"])
X_holdout = vectorizer.transform(holdout_df["text"])

y_train = train_df["label"]
y_synth_test = synth_test_df["label"]
y_holdout = holdout_df["expected_label"]

# ---- Models to compare ----
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": MultinomialNB(),
    "Linear SVM": LinearSVC(),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
}

results = []
trained_models = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    trained_models[name] = model

    synth_acc = accuracy_score(y_synth_test, model.predict(X_synth_test))
    holdout_preds = model.predict(X_holdout)
    holdout_acc = accuracy_score(y_holdout, holdout_preds)

    # Recall on scam class specifically (label=1) - the number that matters most
    scam_report = classification_report(y_holdout, holdout_preds, output_dict=True, zero_division=0)
    scam_recall = scam_report.get("1", {}).get("recall", 0)

    results.append({
        "model": name,
        "synthetic_test_acc": round(synth_acc, 3),
        "REAL_holdout_acc": round(holdout_acc, 3),
        "REAL_scam_recall": round(scam_recall, 3),
    })

# ---- Summary table ----
results_df = pd.DataFrame(results).sort_values("REAL_holdout_acc", ascending=False)
print("\n" + "=" * 70)
print("SUMMARY — sorted by REAL holdout accuracy (the number that matters)")
print("=" * 70)
print(results_df.to_string(index=False))

best_model_name = results_df.iloc[0]["model"]
print(f"\nBest model on real holdout: {best_model_name}")

# ---- Save the best model ----
best_model = trained_models[best_model_name]
joblib.dump(best_model, "ml_classifier.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print(f"Saved best model ({best_model_name}) as ml_classifier.pkl")

# ---- Detailed report for the winning model ----
print(f"\n=== Detailed report for {best_model_name} on REAL holdout ===")
print(classification_report(y_holdout, best_model.predict(X_holdout)))