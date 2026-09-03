from __future__ import annotations

import json
import os
import requests


# ============================================================
# Ollama Configuration
# ============================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5:7b"
)


# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are the final reasoning layer of a Digital Safety Copilot.

Your job is to analyze security evidence collected by other
components of the system and provide a concise, evidence-grounded
explanation for the user.

The input may contain:

1. Text ML evidence
   - scam probability
   - text prediction

2. Rule-based security evidence
   - URL security indicators
   - domain mismatch
   - possible typosquatting
   - suspicious TLD
   - raw IP usage
   - excessive subdomains
   - text-based phishing indicators
   - deterministic risk score
   - triggered flags

3. QR evidence
   - whether a QR code was detected
   - URLs extracted from QR codes
   - URL security evidence for those URLs

IMPORTANT RULES:

- Use ONLY the evidence provided in the JSON.
- Do NOT invent URLs, domains, organizations, threats,
  or security indicators.
- Do NOT independently assume that a domain is malicious.
- Do NOT claim certainty.
- Do NOT override the deterministic risk score.
- The rule engine's risk score and risk level are authoritative
  for the calculated security risk.
- ML probabilities are supporting evidence, not absolute truth.
- Explain WHY the system reached its risk assessment.
- If evidence conflicts, explicitly mention the conflict.
- If evidence is insufficient, say so.
- Never tell the user to click or open a suspicious link.
- For elevated risk, recommend independently verifying the
  organization using an official website, app, or known contact
  method.
- Keep the explanation concise and understandable to a normal user.

Return ONLY valid JSON in exactly this structure:

{
    "risk_level": "LOW|MEDIUM|HIGH|UNKNOWN",
    "explanation": "2-4 concise sentences explaining the result.",
    "safe_actions": [
        "action 1",
        "action 2"
    ],
    "evidence_chain": [
        {
            "step": "string",
            "detail": "string",
            "status": "ok|warning|danger"
        }
    ]
}

The risk_level should normally follow the rule engine's
risk_level when it is available.

Do not generate a numeric risk score.
"""


# ============================================================
# LLM Reasoning Function
# ============================================================

def reason_over_evidence(evidence: dict) -> dict | None:
    """
    Sends the combined evidence JSON to Qwen 2.5 7B through Ollama.

    The evidence should already contain the outputs from:
        - Text ML
        - Rule-based security engine
        - QR extraction
        - URL rule analysis

    Returns the structured LLM response.
    """

    if not isinstance(evidence, dict):
        raise ValueError("evidence must be a dictionary")

    # --------------------------------------------------------
    # Build Ollama request
    # --------------------------------------------------------

    payload = {
        "model": LLM_MODEL,

        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    "Analyze the following security evidence.\n\n"
                    "COMBINED EVIDENCE:\n"
                    + json.dumps(
                        evidence,
                        indent=2,
                        ensure_ascii=False
                    )
                )
            }
        ],

        "stream": False,

        "options": {
            "temperature": 0.1
        },

        "format": "json"
    }

    # --------------------------------------------------------
    # Send request to Ollama
    # --------------------------------------------------------

    try:

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        response_data = response.json()

        content = response_data["message"]["content"].strip()

        # ----------------------------------------------------
        # Parse JSON returned by Qwen
        # ----------------------------------------------------

        result = json.loads(content)

        # ----------------------------------------------------
        # Basic validation
        # ----------------------------------------------------

        if "risk_level" not in result:
            result["risk_level"] = "UNKNOWN"

        if "explanation" not in result:
            result["explanation"] = (
                "The available security evidence was insufficient "
                "to produce a detailed explanation."
            )

        if "safe_actions" not in result:
            result["safe_actions"] = []

        if "evidence_chain" not in result:
            result["evidence_chain"] = []

        return result

    except requests.exceptions.ConnectionError:
        return {
            "risk_level": "UNKNOWN",
            "explanation": (
                "The local Qwen model could not be reached. "
                "Please make sure Ollama is running."
            ),
            "safe_actions": [
                "Start Ollama and run the analysis again."
            ],
            "evidence_chain": [
                {
                    "step": "LLM connection",
                    "detail": "Ollama was not reachable.",
                    "status": "warning"
                }
            ]
        }

    except requests.exceptions.Timeout:
        return {
            "risk_level": "UNKNOWN",
            "explanation": (
                "The local reasoning model took too long to respond."
            ),
            "safe_actions": [
                "Try the analysis again."
            ],
            "evidence_chain": [
                {
                    "step": "LLM response",
                    "detail": "The Ollama request timed out.",
                    "status": "warning"
                }
            ]
        }

    except json.JSONDecodeError:
        return {
            "risk_level": "UNKNOWN",
            "explanation": (
                "The reasoning model returned an invalid response "
                "instead of the expected JSON format."
            ),
            "safe_actions": [
                "Run the analysis again."
            ],
            "evidence_chain": [
                {
                    "step": "LLM output",
                    "detail": "The model response could not be parsed as JSON.",
                    "status": "warning"
                }
            ]
        }

    except Exception as e:
        return {
            "risk_level": "UNKNOWN",
            "explanation": (
                "The final reasoning layer could not complete the analysis."
            ),
            "safe_actions": [
                "Try the analysis again."
            ],
            "evidence_chain": [
                {
                    "step": "LLM processing",
                    "detail": str(e),
                    "status": "warning"
                }
            ]
        }


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    # This represents the COMBINED JSON coming from your
    # ML signal extractor + rule-based security engine.

    sample_evidence = {

        "ml_evidence": {

            "text_scam_probability": 1.0,

            "text_prediction": 1,

            "qr_detected": False,

            "qr_urls": [],

            "qr_data": []
        },

        "security_evidence": {

            "domain_mismatch": True,

            "possible_typosquatting": True,

            "suspicious_tld": True,

            "raw_ip_used": False,

            "excessive_subdomains": False,

            "url_details": [
                {
                    "url": "http://abc-bank-1ogin.xyz/verify"
                }
            ],

            "urgency": True,

            "credential_request": True,

            "threat_detected": True,

            "reward_bait": False,

            "excessive_punctuation": True,

            "matched_phrases": [
                "URGENT",
                "account will be blocked",
                "verify your password"
            ],

            "risk_level": "HIGH",

            "triggered_flags": [
                "DOMAIN_MISMATCH",
                "POSSIBLE_TYPOSQUATTING",
                "SUSPICIOUS_TLD",
                "CREDENTIAL_REQUEST",
                "URGENCY"
            ]
        }
    }

    result = reason_over_evidence(sample_evidence)

    print("\n" + "=" * 60)
    print("QWEN 2.5 7B REASONING RESULT")
    print("=" * 60)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )