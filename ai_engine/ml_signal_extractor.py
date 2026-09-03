import sys
import os
import joblib

# Make ml_engine importable regardless of where this script is run from
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "ml_engine")
)

from qr import analyze_screenshot_qr


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_TEXT_MODEL_PATH = os.path.join(
    BASE_DIR, "ml_engine", "ml_classifier.pkl"
)

_VECTORIZER_PATH = os.path.join(
    BASE_DIR, "ml_engine", "vectorizer.pkl"
)

_text_model = None
_vectorizer = None


def _load_text_model():
    global _text_model, _vectorizer

    if _text_model is None:
        _text_model = joblib.load(_TEXT_MODEL_PATH)
        _vectorizer = joblib.load(_VECTORIZER_PATH)

    return _text_model, _vectorizer


def score_text(text: str) -> dict:
    """
    ML analysis for TEXT ONLY.

    URL analysis is intentionally NOT done here.
    URLs are handled by the rule-based security engine.
    """

    if not text:
        return {
            "text_scam_probability": None,
            "text_prediction": None
        }

    model, vectorizer = _load_text_model()

    vec = vectorizer.transform([text])

    prob = model.predict_proba(vec)[0][1]
    pred = int(model.predict(vec)[0])

    return {
        "text_scam_probability": round(float(prob), 3),
        "text_prediction": pred
    }


def get_ml_evidence(extracted_data: dict) -> dict:
    """
    ML evidence layer.

    ML is used ONLY for text classification.

    URLs are deliberately NOT scored here because URL analysis
    is handled by the rule-based security engine.

    QR codes are decoded here, but their URLs are NOT classified here.
    The extracted QR URLs are passed to the rule engine.
    """

    text = extracted_data.get("extracted_text", "") or ""
    image_path = extracted_data.get("image_path")

    # ---------------------------------------------------------
    # 1. TEXT ML
    # ---------------------------------------------------------

    text_result = score_text(text)

    # ---------------------------------------------------------
    # 2. QR DETECTION / EXTRACTION
    # ---------------------------------------------------------

    qr_detected = False
    qr_urls = []
    qr_data = []

    if image_path:
        qr_result = analyze_screenshot_qr(image_path)

        qr_detected = qr_result.get("qr_codes_found", 0) > 0
        qr_urls = qr_result.get("extracted_urls", [])
        qr_data = qr_result.get("qr_data", [])

    # ---------------------------------------------------------
    # 3. RETURN ONLY ML + QR SIGNALS
    # ---------------------------------------------------------

    return {
        "text_scam_probability": text_result["text_scam_probability"],
        "text_prediction": text_result["text_prediction"],

        # QR detection is extraction, not ML classification
        "qr_detected": qr_detected,
        "qr_urls": qr_urls,
        "qr_data": qr_data
    }


if __name__ == "__main__":

    import json

    sample_input = {
        "extracted_text":
            "URGENT! Your account will be blocked. "
            "Verify your password now!!!",

        "urls": [
            "http://abc-bank-1ogin.xyz/verify"
        ],

        "image_path": None
    }

    result = get_ml_evidence(sample_input)

    print(json.dumps(result, indent=2))