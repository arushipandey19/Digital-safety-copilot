"""
url_analyzer.py

The main entry point for URL-based security checks. This is the file
that the rest of the pipeline (Arushi's pipeline_service.py) will call.

Input (from the extraction layer):
    {
        "urls": ["http://abc-bank-1ogin.xyz/verify"],
        "claimed_organization": "ABC Bank"
    }

Output (sent forward to the correlation layer, once that's built):
    {
        "urls_analyzed": ["http://abc-bank-1ogin.xyz/verify"],
        "domain_mismatch": True,
        "possible_typosquatting": True,
        "suspicious_tld": True,
        "raw_ip_used": False,
        "excessive_subdomains": False,
        "details": [ ... ]
    }
"""

import re
from urllib.parse import urlparse

try:
    from .domain_checker import check_organization_domain_match
    from .typosquatting import check_typosquatting
except ImportError:
    # Allows running this file directly for testing
    from domain_checker import check_organization_domain_match
    from typosquatting import check_typosquatting


# TLDs that are cheap/anonymous and commonly abused in phishing campaigns.
# Not proof of phishing by itself, just one signal among many.
SUSPICIOUS_TLDS = {".xyz", ".tk", ".ml", ".ga", ".cf", ".gq", ".top", ".club", ".info"}

# A domain with more than this many subdomain levels is unusual and
# often used to hide the real domain, e.g. "login.secure.abc.bank.xyz"
MAX_NORMAL_SUBDOMAINS = 2

IP_PATTERN = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


def extract_domain(url: str) -> str:
    """
    Pulls just the domain out of a full URL.
    "http://abc-bank-1ogin.xyz/verify?id=1" -> "abc-bank-1ogin.xyz"
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url  # urlparse needs a scheme to work correctly

    parsed = urlparse(url)
    return parsed.netloc.lower()


def has_suspicious_tld(domain: str) -> bool:
    return any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)


def uses_raw_ip(domain: str) -> bool:
    return bool(IP_PATTERN.match(domain))


def has_excessive_subdomains(domain: str) -> bool:
    # e.g. "login.secure.verify.abc-bank.xyz" -> 4 parts before the TLD
    parts = domain.split(".")
    return len(parts) - 2 > MAX_NORMAL_SUBDOMAINS  # -2 excludes domain + TLD


def analyze_url(url: str, claimed_organization: str = None) -> dict:
    """
    Runs every URL-level check on a single URL and returns one combined
    evidence dictionary for it.
    """
    domain = extract_domain(url)

    domain_match_result = check_organization_domain_match(claimed_organization, domain)
    typo_result = check_typosquatting(domain)

    return {
        "url": url,
        "domain": domain,
        "domain_verified": domain_match_result["domain_verified"],
        "domain_mismatch": domain_match_result["domain_mismatch"],
        "domain_mismatch_reason": domain_match_result["reason"],
        "possible_typosquatting": typo_result["possible_typosquatting"],
        "closest_verified_domain": typo_result["closest_verified_domain"],
        "typosquatting_similarity": typo_result["similarity_score"],
        "suspicious_tld": has_suspicious_tld(domain),
        "raw_ip_used": uses_raw_ip(domain),
        "excessive_subdomains": has_excessive_subdomains(domain),
    }


def analyze_urls(urls: list, claimed_organization: str = None) -> dict:
    """
    This is the function the pipeline actually calls.
    Runs analyze_url() on every URL found in the message and
    combines them into one summary result.

    If there are no URLs at all, all flags default to False.
    """
    if not urls:
        return {
            "urls_analyzed": [],
            "domain_mismatch": False,
            "possible_typosquatting": False,
            "suspicious_tld": False,
            "raw_ip_used": False,
            "excessive_subdomains": False,
            "details": [],
        }

    details = [analyze_url(url, claimed_organization) for url in urls]

    # If ANY url in the message trips a flag, we raise that flag overall.
    # (A message is dangerous if even one of its links is malicious.)
    return {
        "urls_analyzed": urls,
        "domain_mismatch": any(d["domain_mismatch"] for d in details),
        "possible_typosquatting": any(d["possible_typosquatting"] for d in details),
        "suspicious_tld": any(d["suspicious_tld"] for d in details),
        "raw_ip_used": any(d["raw_ip_used"] for d in details),
        "excessive_subdomains": any(d["excessive_subdomains"] for d in details),
        "details": details,
    }


if __name__ == "__main__":
    # Quick manual test matching the example from our planning discussion
    result = analyze_urls(
        urls=["http://abc-bank-1ogin.xyz/verify"],
        claimed_organization="ABC Bank",
    )
    import json
    print(json.dumps(result, indent=2))