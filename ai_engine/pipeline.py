"""
pipeline.py
------------
Lives in ai_engine/, alongside ml_signal_extractor.py, rule_engine.py, llm.py.

This is the ONLY new logic in this file: call all three, merge, return.
No FastAPI, no frontend concerns - that's Member 2's job.

Input (same "extracted_data" contract both ml_signal_extractor.py and
rule_engine.py already expect):
    {
        "extracted_text": str,
        "urls": list[str],
        "claimed_organization": str | None,
        "image_path": str | None
    }

Output: the final structured JSON from the LLM reasoning layer -
    {
        "risk_level": "LOW|MEDIUM|HIGH|UNKNOWN",
        "explanation": "...",
        "safe_actions": [...],
        "evidence_chain": [...]
    }
"""

from ml_signal_extractor import get_ml_evidence
from rule_engine import run_security_engine
from llm import reason_over_evidence


def analyze(extracted_data: dict) -> dict:
    """
    The single function Member 2's backend will call.
    """

    # 1. Get ML evidence (text classifier + QR detection)
    ml_evidence = get_ml_evidence(extracted_data)

    # 2. Get rule-based evidence (URL analysis + phishing text rules)
    security_evidence = run_security_engine(extracted_data)

    # 3. Merge into one combined evidence dict
    combined_evidence = {
        "ml_evidence": ml_evidence,
        "security_evidence": security_evidence,
    }

    # 4. Send to the LLM correlation/reasoning layer
    final_result = reason_over_evidence(combined_evidence)

    return final_result


if __name__ == "__main__":
    import json

    # Same style sample input the other three files already test with,
    # so results are directly comparable to their individual __main__ runs
    sample_input = {
        "extracted_text": "URGENT! Your account will be blocked. Verify your password now!!!",
        "urls": ["http://abc-bank-1ogin.xyz/verify"],
        "claimed_organization": "ABC Bank",
        "image_path": None,
    }

    result = analyze(sample_input)

    print("\n" + "=" * 60)
    print("FULL PIPELINE RESULT")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))