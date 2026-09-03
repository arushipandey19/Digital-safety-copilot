"""
typosquatting.py

Detects "typosquatting" — domains that are deliberately spelled to look
almost identical to a real, trusted domain, e.g.:

    hdfcbank.com   (real)
    hdfcbnk.com    (missing letter)
    hdfcbank1.com  (extra character)
    hdfcbank-login.com (added word)
    hdfcbаnk.com   (lookalike character trick)

We use simple string-similarity (difflib) instead of ML here, so the
result stays explainable: "this domain is 90% similar to hdfcbank.com".
"""

import difflib

try:
    from .domain_checker import load_verified_domains, is_domain_verified
except ImportError:
    # Allows running this file directly (python typosquatting.py) for testing
    from domain_checker import load_verified_domains, is_domain_verified


# Below this similarity score, we don't consider it "close enough" to flag
SIMILARITY_THRESHOLD = 0.6


def _domain_root(domain: str) -> str:
    """
    Strips the domain down to its main name, ignoring the TLD, so
    "hdfcbank.com" and "hdfcbank.xyz" compare on "hdfcbank".
    """
    parts = domain.lower().split(".")
    if len(parts) >= 2:
        return parts[-2]  # second-to-last part, e.g. "hdfcbank" in "www.hdfcbank.com"
    return domain.lower()


def check_typosquatting(domain: str) -> dict:
    """
    Compares `domain` against every verified domain and returns the
    closest match, along with whether it looks suspicious.

    Returns:
        {
            "possible_typosquatting": True,
            "closest_verified_domain": "hdfcbank.com",
            "similarity_score": 0.89
        }
    """
    domain = domain.lower()

    # If it's already an exact verified domain, it can't be typosquatting
    if is_domain_verified(domain):
        return {
            "possible_typosquatting": False,
            "closest_verified_domain": None,
            "similarity_score": 0.0,
        }

    domain_root = _domain_root(domain)
    verified_domains = load_verified_domains()

    best_match = None
    best_score = 0.0

    for verified in verified_domains:
        verified_root = _domain_root(verified)

        score = difflib.SequenceMatcher(None, domain_root, verified_root).ratio()

        if score > best_score:
            best_score = score
            best_match = verified

    # High similarity but NOT an exact/verified match = classic typosquatting
    is_suspicious = best_score >= SIMILARITY_THRESHOLD

    return {
        "possible_typosquatting": is_suspicious,
        "closest_verified_domain": best_match if is_suspicious else None,
        "similarity_score": round(best_score, 2),
    }


if __name__ == "__main__":
    # Quick manual tests
    print(check_typosquatting("hdfcbnk-login.com"))   # should flag
    print(check_typosquatting("paytm.com"))            # verified, no flag
    print(check_typosquatting("randomsite123.xyz"))    # not similar, no flag