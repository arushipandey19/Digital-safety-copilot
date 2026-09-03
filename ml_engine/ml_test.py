"""
Batch test the trained text classifier against labeled test messages.

Usage:
    python test_text_classifier.py test_messages_batch1.csv
"""

import sys
import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_text_classifier.py <test_messages.csv>")
        sys.exit(1)

    test_path = sys.argv[1]
    df = pd.read_csv(test_path)

    model = joblib.load("ml_classifier.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    X = vectorizer.transform(df["text"])
    preds = model.predict(X)
    probs = model.predict_proba(X)

    df["predicted_label"] = preds
    df["confidence"] = probs.max(axis=1)
    df["correct"] = df["predicted_label"] == df["expected_label"]

    print("\n=== Results per message ===")
    for _, row in df.iterrows():
        mark = "OK " if row["correct"] else "MISS"
        print(f"[{mark}] expected={row['expected_label']} predicted={row['predicted_label']} "
              f"(conf {row['confidence']:.2f}) [{row['category']}] {row['text'][:60]}")

    accuracy = df["correct"].mean()
    print(f"\nOverall accuracy on this batch: {accuracy:.2%} ({df['correct'].sum()}/{len(df)})")

    print("\n=== Classification report ===")
    print(classification_report(df["expected_label"], df["predicted_label"]))

    print("Confusion matrix:")
    print(confusion_matrix(df["expected_label"], df["predicted_label"]))

    print("\n=== Missed cases (worth reviewing) ===")
    misses = df[~df["correct"]]
    if len(misses) == 0:
        print("None — all correct!")
    else:
        for _, row in misses.iterrows():
            print(f"  category={row['category']} expected={row['expected_label']} "
                  f"got={row['predicted_label']} text=\"{row['text']}\"")

if __name__ == "__main__":
    main()