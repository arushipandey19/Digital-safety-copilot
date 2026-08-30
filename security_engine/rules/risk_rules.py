"""
risk_rules.py

Turns all the individual True/False flags (from phishing_rules.py and
url_analyzer.py) into ONE combined risk score and risk level.

This is a deterministic, rule-based score — it does NOT use the LLM.
That matters for the project's pitch: we can show judges a risk score
that exists even before the LLM correlation layer runs, because it's
just weighted arithmetic over evidence, not a black box.

The LLM correlation layer (built later, by the team) will take this
score plus the ML model's prediction and produce the FINAL explained
verdict — this module just handles the security-engine's own opinion.
"""

# How much each flag contributes to the total risk score (out of 100).
# Feel free to tune these weights once you have real test examples.
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

# Score ranges mapped to a human-readable risk level
def _score_to_level(score: int) -> str:
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_risk_score(url_evidence: dict, text_evidence: dict) -> dict:
    """
    Combines URL evidence (from url_analyzer.analyze_urls) and text
    evidence (from phishing_rules.run_all_phishing_rules) into one
    risk score.

    Example inputs:
        url_evidence = {"domain_mismatch": True, "possible_typosquatting": True, ...}
        text_evidence = {"urgency": True, "credential_request": True, ...}

    Returns:
        {
            "risk_score": 75,
            "risk_level": "HIGH",
            "triggered_flags": ["domain_mismatch", "possible_typosquatting", "urgency", "credential_request"]
        }
    """
    combined_flags = {**url_evidence, **text_evidence}

    score = 0
    triggered = []

    for flag_name, weight in WEIGHTS.items():
        if combined_flags.get(flag_name) is True:
            score += weight
            triggered.append(flag_name)

    # Cap at 100 in case weights overlap oddly
    score = min(score, 100)

    return {
        "risk_score": score,
        "risk_level": _score_to_level(score),
        "triggered_flags": triggered,
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

    import json
    print(json.dumps(calculate_risk_score(sample_url_evidence, sample_text_evidence), indent=2))