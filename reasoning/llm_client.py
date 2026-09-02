from __future__ import annotations
import json
import os
import requests


def reason_over_evidence(evidence: dict) -> dict | None:
    """Final evidence-grounded reasoning layer using an OpenAI-compatible endpoint."""

    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")

    if not all([base_url, api_key, model]):
        return None

    system_prompt = """
You are the final reasoning layer of a digital safety copilot.

Use ONLY the supplied evidence from OCR, QR decoding, URL/security rules,
ML and vision observations.

Return ONLY valid JSON:
{
  "risk_level": "LOW|MEDIUM|HIGH",
  "explanation": "2-4 concise sentences",
  "safe_actions": ["..."],
  "evidence_chain": [
    {"step":"string","detail":"string","status":"ok|warning|danger"}
  ]
}

Rules:
- Do not invent facts.
- Do not claim certainty.
- Do not say the message is definitely malicious.
- The numeric risk score is produced by deterministic code, not by you.
- Prefer independent verification when risk is elevated.
"""

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "Evidence:\n" +
                           json.dumps(
                               evidence,
                               indent=2,
                               ensure_ascii=False
                           )
            }
        ],
        "temperature": 0.1,
        "max_tokens": 900
    }

    try:
        r = requests.post(
            base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=45
        )

        r.raise_for_status()

        content = r.json()["choices"][0]["message"]["content"].strip()
        content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except Exception:
        return None