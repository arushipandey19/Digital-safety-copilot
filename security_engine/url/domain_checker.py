"""
domain_checker.py

Responsible for:
1. Loading the verified_domains/domains.json list
2. Checking whether a given domain is "verified" (i.e. a known, trusted domain)
3. Checking whether a message's claimed organization matches the domain
   actually used in the URL (a classic phishing red flag)

This module is deliberately simple and rule-based (no ML here) so its
output is explainable — we can always say *why* a flag was raised.
"""

import json
import os
import re

# Path to the domains.json file, relative to this file's location
DOMAINS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "verified_domains", "domains.json"
)


def load_verified_domains():
    """
    Loads domains.json and returns a flat set of all verified domains,
    e.g. {"hdfcbank.com", "paytm.com", ...}
    """
    with open(DOMAINS_FILE, "r") as f:
        data = json.load(f)

    flat_domains = set()
    for category, domain_list in data.items():
        for domain in domain_list:
            flat_domains.add(domain.lower())

    return flat_domains


def is_domain_verified(domain: str) -> bool:
    """
    Returns True if `domain` exactly matches something in our verified list.

    Example:
        is_domain_verified("paytm.com") -> True
        is_domain_verified("paytm-secure-login.xyz") -> False
    """
    verified = load_verified_domains()
    return domain.lower() in verified


def _normalize(text: str) -> str:
    """
    Strips a string down to just lowercase letters/numbers, so
    "ABC Bank" and "abc-bank" and "abcbank" all normalize to "abcbank".
    Makes comparison easier and more forgiving.
    """
    return re.sub(r"[^a-z0-9]", "", text.lower())


def check_organization_domain_match(claimed_organization: str, domain: str) -> dict:
    """
    Checks whether the organization the message CLAIMS to be from
    matches the domain that was ACTUALLY used.

    Example:
        claimed_organization = "ABC Bank"
        domain = "abc-bank-login.xyz"

        -> domain is NOT in our verified list
        -> but the domain text does contain "abcbank"
        -> so this looks like impersonation, not just an unknown domain

    Returns a dict like:
        {
            "domain_verified": False,
            "domain_mismatch": True,
            "reason": "Claimed organization 'ABC Bank' does not match verified domain for this brand"
        }
    """
    domain = domain.lower()
    verified = is_domain_verified(domain)

    result = {
        "domain_verified": verified,
        "domain_mismatch": False,
        "reason": None,
    }

    if verified:
        # Domain is directly on our trusted list, no mismatch possible
        return result

    if not claimed_organization:
        # We don't know who the message claims to be from, so we can only
        # say the domain is unverified, not that it's a mismatch.
        result["reason"] = "Domain is not on the verified list (no claimed organization given)"
        return result

    org_normalized = _normalize(claimed_organization)
    domain_normalized = _normalize(domain)

    # If the org name shows up inside an UNVERIFIED domain, that's a strong
    # impersonation signal (e.g. "abcbank" inside "abc-bank-login.xyz")
    if org_normalized and org_normalized in domain_normalized:
        result["domain_mismatch"] = True
        result["reason"] = (
            f"Claimed organization '{claimed_organization}' appears in the domain, "
            f"but '{domain}' is not a verified domain for this brand"
        )
    else:
        result["domain_mismatch"] = True
        result["reason"] = (
            f"Claimed organization '{claimed_organization}' does not match "
            f"unverified domain '{domain}'"
        )

    return result


if __name__ == "__main__":
    # Quick manual test
    print(check_organization_domain_match("ABC Bank", "abc-bank-login.xyz"))
    print(check_organization_domain_match("Paytm", "paytm.com"))