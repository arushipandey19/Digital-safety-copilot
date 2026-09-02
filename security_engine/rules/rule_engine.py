"""
rule_engine.py

This is the MAIN entry point for the whole Security Engine.
Arushi's pipeline_service.py should only ever need to call ONE function
from your entire module: run_security_engine().

It orchestrates:
    1. url_analyzer.py       -> URL-based evidence
    2. phishing_rules.py     -> text-based evidence
    3. risk_rules.py         -> combines both into one risk score

Input (from the extraction layer):
    {
        "extracted_text": "URGENT! Your account will be blocked. Verify now.",
        "urls": ["http://abc-bank-1ogin.xyz/verify"],
        "claimed_organization": "ABC Bank"
    }

Output (the full "security_evidence" block that later goes to the
LLM correlation layer, once that's built by the team):
    {
        "domain_mismatch": True,
        "possible_typosquatting": True,
        "suspicious_tld": True,
        "raw_ip_used": False,
        "excessive_subdomains": False,
        "urgency": True,
        "credential_request": True,
        "threat_detected": False,
        "reward_bait": False,
        "excessive_punctuation": True,
        "matched_phrases": ["urgent", "verify your password"],
        "risk_score": 90,
        "risk_level": "HIGH",
        "triggered_flags": [...],
        "url_details": [...]
    }
"""

import sys
import os

# Make sibling packages (url/) importable whether this file is run
# directly or imported as part of the security_engine package.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "url"))

try:
    from ..url.url_analyzer import analyze_urls
except (ImportError, ValueError):
    from url_analyzer import analyze_urls

from .phishing_rules import run_all_phishing_rules
from .risk_rules import calculate_risk_score


def run_security_engine(extracted_data: dict) -> dict:
    """
    The single function the rest of the team's pipeline calls.

    extracted_data must contain:
        - "extracted_text": str
        - "urls": list[str]  (can be empty)
        - "claimed_organization": str | None
    """
    text = extracted_data.get("extracted_text", "") or ""
    urls = extracted_data.get("urls", []) or []
    claimed_organization = extracted_data.get("claimed_organization")

    url_evidence = analyze_urls(urls, claimed_organization)
    text_evidence = run_all_phishing_rules(text)

    risk_result = calculate_risk_score(url_evidence, text_evidence)

    # Combine everything into one flat evidence dict for the correlation layer
    security_evidence = {
        # URL flags
        "domain_mismatch": url_evidence["domain_mismatch"],
        "possible_typosquatting": url_evidence["possible_typosquatting"],
        "suspicious_tld": url_evidence["suspicious_tld"],
        "raw_ip_used": url_evidence["raw_ip_used"],
        "excessive_subdomains": url_evidence["excessive_subdomains"],
        "url_details": url_evidence["details"],
        # Text flags
        "urgency": text_evidence["urgency"],
        "credential_request": text_evidence["credential_request"],
        "threat_detected": text_evidence["threat_detected"],
        "reward_bait": text_evidence["reward_bait"],
        "excessive_punctuation": text_evidence["excessive_punctuation"],
        "matched_phrases": text_evidence["matched_phrases"],
        # Combined risk score (rule-based only, not LLM)
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "triggered_flags": risk_result["triggered_flags"],
    }

    return security_evidence


if __name__ == "__main__":
    # End-to-end test matching our planning example
    sample_input = {
        "extracted_text": "URGENT! Your account will be blocked. Verify your password now!!!",
        "urls": ["http://abc-bank-1ogin.xyz/verify"],
        "claimed_organization": "ABC Bank",
    }

    import json
    result = run_security_engine(sample_input)
    print(json.dumps(result, indent=2))