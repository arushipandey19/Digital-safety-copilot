import sys
import os

# This file lives in ai_engine/. The rule modules it needs live in
# security_engine/rules/ and security_engine/url/ - both are siblings
# of ai_engine at the project root level, so we go up one and back down.
_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")

sys.path.append(os.path.join(_PROJECT_ROOT, "security_engine", "url"))
sys.path.append(os.path.join(_PROJECT_ROOT, "security_engine", "rules"))

from url_analyser import analyze_urls          # security_engine/url/url_analyser.py
from phishing_rules import run_all_phishing_rules  # security_engine/rules/phishing_rules.py
from risk_rules import calculate_risk_score        # security_engine/rules/risk_rules.py


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