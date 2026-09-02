"""
phishing_rules.py

Deterministic, keyword/pattern-based checks on the MESSAGE TEXT
(as opposed to url_analyzer.py, which checks the URLs).

Each function returns True/False plus which phrase(s) triggered it,
so the final result stays explainable.
"""

import re

URGENCY_PATTERNS = [
    "urgent", "act now", "immediately", "act immediately",
    "account will be blocked", "account will be suspended",
    "expires today", "expires in", "limited time", "final notice",
    "last warning", "within 24 hours", "verify now",
]

CREDENTIAL_REQUEST_PATTERNS = [
    "verify your password", "enter your otp", "confirm your pin",
    "update your card details", "enter your cvv", "confirm your password",
    "verify your account", "login to confirm", "provide your card number",
    "share your otp", "enter your bank details",
]

THREAT_PATTERNS = [
    "account will be suspended", "legal action will be taken",
    "unauthorized login detected", "your account has been compromised",
    "suspicious activity detected", "account permanently disabled",
    "failure to comply", "penalty will be charged",
]

REWARD_BAIT_PATTERNS = [
    "you've won", "you have won", "claim your prize", "free gift",
    "congratulations you", "lucky winner", "cashback offer",
    "click to claim", "limited time offer", "exclusive reward",
]


def _find_matches(text: str, patterns: list) -> list:
    """Returns the list of patterns found in `text` (case-insensitive)."""
    text_lower = text.lower()
    return [p for p in patterns if p in text_lower]


def check_urgency(text: str) -> dict:
    matches = _find_matches(text, URGENCY_PATTERNS)
    return {"urgency": len(matches) > 0, "matched_phrases": matches}


def check_credential_request(text: str) -> dict:
    matches = _find_matches(text, CREDENTIAL_REQUEST_PATTERNS)
    return {"credential_request": len(matches) > 0, "matched_phrases": matches}


def check_threat(text: str) -> dict:
    matches = _find_matches(text, THREAT_PATTERNS)
    return {"threat_detected": len(matches) > 0, "matched_phrases": matches}


def check_reward_bait(text: str) -> dict:
    matches = _find_matches(text, REWARD_BAIT_PATTERNS)
    return {"reward_bait": len(matches) > 0, "matched_phrases": matches}


def check_excessive_punctuation(text: str) -> dict:
    """
    Phishing/spam text often overuses exclamation marks or ALL CAPS
    to create urgency/alarm, e.g. "URGENT!!! VERIFY NOW!!!"
    """
    exclamations = text.count("!")
    caps_words = re.findall(r"\b[A-Z]{4,}\b", text)  # words of 4+ capital letters
    return {
        "excessive_punctuation": exclamations >= 2 or len(caps_words) >= 2,
        "exclamation_count": exclamations,
        "all_caps_words": caps_words,
    }


def run_all_phishing_rules(text: str) -> dict:
    """
    Runs every text-based rule and returns one combined dictionary.
    This is what rule_engine.py calls.
    """
    urgency = check_urgency(text)
    credential = check_credential_request(text)
    threat = check_threat(text)
    reward = check_reward_bait(text)
    punctuation = check_excessive_punctuation(text)

    return {
        "urgency": urgency["urgency"],
        "credential_request": credential["credential_request"],
        "threat_detected": threat["threat_detected"],
        "reward_bait": reward["reward_bait"],
        "excessive_punctuation": punctuation["excessive_punctuation"],
        "matched_phrases": (
            urgency["matched_phrases"]
            + credential["matched_phrases"]
            + threat["matched_phrases"]
            + reward["matched_phrases"]
        ),
    }


if __name__ == "__main__":
    sample = "URGENT! Your account will be blocked. Verify your password now!!!"
    import json
    print(json.dumps(run_all_phishing_rules(sample), indent=2))
    