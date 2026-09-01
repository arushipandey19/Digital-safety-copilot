"""
URL Phishing Classifier
------------------------
Trains a model to classify URLs as phishing (1) or benign (0).

Works two ways:
1. If your CSV already has numeric features + a label column (e.g. URL-Phish
   dataset with 22 engineered features) -> uses those directly.
2. If your CSV only has raw URLs + label -> extracts features itself using
   extract_url_features() below, so it still works with a simple
   "url,label" style dataset (like common Kaggle phishing URL sets).

Usage:
    python train_url_classifier.py your_url_dataset.csv
"""

import sys
import re
import pandas as pd
import joblib
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "bank", "confirm",
    "kyc", "otp", "payment", "refund", "suspend", "block", "signin"
]

SHORTENERS = ["bit.ly", "tinyurl", "t.co", "goo.gl", "is.gd", "cutt.ly"]


def extract_url_features(url: str) -> dict:
    """Turn a raw URL string into numeric features a model can use."""
    url = str(url)
    parsed = urlparse(url if "://" in url else "http://" + url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    full = url.lower()

    return {
        "url_length": len(url),
        "domain_length": len(domain),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(c.isdigit() for c in url),
        "num_subdomains": max(domain.count(".") - 1, 0),
        "has_ip_address": 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain) else 0,
        "has_https": 1 if parsed.scheme == "https" else 0,
        "has_at_symbol": 1 if "@" in url else 0,
        "has_shortener": 1 if any(s in domain for s in SHORTENERS) else 0,
        "num_suspicious_keywords": sum(kw in full for kw in SUSPICIOUS_KEYWORDS),
        "path_length": len(path),
        "num_slashes": url.count("/"),
        "has_double_slash_redirect": 1 if "//" in path else 0,
        "num_special_chars": len(re.findall(r"[^a-zA-Z0-9./:-]", url)),
    }


def load_and_prepare(csv_path: str):
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]

    if "label" not in df.columns:
        raise ValueError("CSV must have a 'label' column (0 = benign, 1 = phishing).")

    # Case 1: URL-Phish dataset (data.mendeley.com/datasets/65z9twcx3r) has
    # exactly these non-feature columns: url, dom (domain), tld, label.
    # Everything else in the file is one of the 22 engineered numeric features.
    non_feature_cols = {"label", "url", "domain", "dom", "tld", "id"}
    numeric_cols = [c for c in df.columns
                    if c not in non_feature_cols and pd.api.types.is_numeric_dtype(df[c])]

    if len(numeric_cols) >= 5:
        print(f"Using {len(numeric_cols)} existing numeric feature columns from the dataset.")
        print(f"(Detected as URL-Phish-style dataset — reference cols excluded: "
              f"{[c for c in df.columns if c in non_feature_cols]})")
        X = df[numeric_cols].fillna(0)
        y = df["label"]
        return X, y, numeric_cols

    # Case 2: only raw URLs -> extract features ourselves
    url_col = "url" if "url" in df.columns else df.columns[0]
    print(f"No engineered features found — extracting features from '{url_col}' column.")
    features = df[url_col].apply(extract_url_features).apply(pd.Series)
    X = features.fillna(0)
    y = df["label"]
    return X, y, list(X.columns)


def main():
    if len(sys.argv) < 2:
        print("Usage: python train_url_classifier.py <path_to_url_dataset.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    X, y, feature_names = load_and_prepare(csv_path)

    print("\nClass balance:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200, max_depth=None, random_state=42, n_jobs=-1, class_weight="balanced"
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("\n=== Test set performance ===")
    print(classification_report(y_test, preds))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, preds))

    # Feature importance — useful to show judges WHY the model flags a URL
    importances = pd.Series(model.feature_importances_, index=feature_names)
    print("\nTop 10 most important features:")
    print(importances.sort_values(ascending=False).head(10))

    joblib.dump(model, "url_classifier.pkl")
    joblib.dump(feature_names, "url_feature_names.pkl")
    print("\nSaved: url_classifier.pkl, url_feature_names.pkl")


def predict_single_url(url: str, model_path="url_classifier.pkl",
                        feature_names_path="url_feature_names.pkl"):
    """Use this in your FastAPI backend to score one URL at request time."""
    model = joblib.load(model_path)
    feature_names = joblib.load(feature_names_path)
    feats = extract_url_features(url)
    row = pd.DataFrame([{k: feats.get(k, 0) for k in feature_names}])
    prob = model.predict_proba(row)[0][1]  # probability of phishing
    return {"url": url, "phishing_probability": round(float(prob), 3)}


if __name__ == "__main__":
    main()