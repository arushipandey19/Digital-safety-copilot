WEIGHTS = {
    # from url_analyzer.py
    "domain_mismatch": 25,
    "possible_typosquatting": 20,
    "suspicious_tld": 10,
    "raw_ip_used": 15,
    "excessive_subdomains": 5,
    # from phishing_rules.py
    "urgency": 10,
    "credential_request": 20,
    "threat_detected": 15,
    "reward_bait": 10,
    "excessive_punctuation": 5,
}

# How much the ML text classifier's probability can contribute to the
# score on its own, scaled linearly. A message with no rule flags at all
# can still reach HIGH risk if the ML model is confident enough - this
# is what was missing before, causing 99%+ scam probabilities to be
# rated LOW when no URL/rule flags happened to trigger.
ML_MAX_CONTRIBUTION = 45


# Score ranges mapped to a human-readable risk level
def _score_to_level(score: int) -> str:
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_risk_score(url_evidence: dict, text_evidence: dict, ml_evidence: dict = None) -> dict:
    """
    Combines URL evidence (from url_analyzer.analyze_urls), text
    evidence (from phishing_rules.run_all_phishing_rules), AND the
    ML text classifier's scam probability into one risk score.

    ml_evidence is optional for backward compatibility, but should be
    passed as {"text_scam_probability": 0.0-1.0} whenever available -
    without it, this function silently ignores the ML signal entirely,
    which was the original bug.

    Example inputs:
        url_evidence = {"domain_mismatch": True, "possible_typosquatting": True, ...}
        text_evidence = {"urgency": True, "credential_request": True, ...}
        ml_evidence = {"text_scam_probability": 0.992}

    Returns:
        {
            "risk_score": 75,
            "risk_level": "HIGH",
            "triggered_flags": ["domain_mismatch", "possible_typosquatting", "urgency", "credential_request"],
            "ml_contribution": 44
        }
    """
    combined_flags = {**url_evidence, **text_evidence}

    score = 0
    triggered = []

    for flag_name, weight in WEIGHTS.items():
        if combined_flags.get(flag_name) is True:
            score += weight
            triggered.append(flag_name)

    # ---- NEW: fold in the ML text scam probability ----
    ml_contribution = 0
    if ml_evidence:
        prob = ml_evidence.get("text_scam_probability")
        if prob is not None:
            ml_contribution = round(prob * ML_MAX_CONTRIBUTION)
            score += ml_contribution
            if prob >= 0.85:
                triggered.append("high_ml_scam_probability")

    # Cap at 100 in case weights overlap oddly
    score = min(score, 100)

    return {
        "risk_score": score,
        "risk_level": _score_to_level(score),
        "triggered_flags": triggered,
        "ml_contribution": ml_contribution,
    }


if __name__ == "__main__":
    sample_url_evidence = {
        "domain_mismatch": True,
        "possible_typosquatting": True,
        "suspicious_tld": True,
        "raw_ip_used": False,
        "excessive_subdomains": False,
    }
    sample_text_evidence = {
        "urgency": True,
        "credential_request": True,
        "threat_detected": False,
        "reward_bait": False,
        "excessive_punctuation": True,
    }
    sample_ml_evidence = {
        "text_scam_probability": 0.992,
    }

    import json
    print("With ML evidence:")
    print(json.dumps(
        calculate_risk_score(sample_url_evidence, sample_text_evidence, sample_ml_evidence),
        indent=2
    ))

    print("\nWithout ML evidence (old behavior, for comparison):")
    print(json.dumps(
        calculate_risk_score(sample_url_evidence, sample_text_evidence),
        indent=2
    ))

    print("\nHigh ML probability, but ZERO rule flags (the exact bug from your screenshots):")
    print(json.dumps(
        calculate_risk_score(
            {"domain_mismatch": False, "possible_typosquatting": False, "suspicious_tld": False,
             "raw_ip_used": False, "excessive_subdomains": False},
            {"urgency": False, "credential_request": False, "threat_detected": False,
             "reward_bait": False, "excessive_punctuation": False},
            {"text_scam_probability": 0.999}
        ),
        indent=2
    ))