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
    Internal entry point. Expects the ai_engine contract exactly:
        {"extracted_text": str, "urls": list[str],
         "claimed_organization": str|None, "image_path": str|None}
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


def analyze_from_extraction(extraction_output: dict, image_path: str = None) -> dict:
    """
    THE FUNCTION MEMBER 2 SHOULD CALL.

    Accepts pipeline_service.run_pipeline()'s actual output shape as-is:
        {
            "input_type": str,
            "text": str,
            "urls": list[str],
            "claimed_organization": str,
            "entities": {"phone_numbers": [...], "emails": [...]}
        }

    Bridges the field-name difference ("text" -> "extracted_text")
    internally, so Member 2 never needs to know or care about the
    ai_engine contract's exact key names - they just pass their own
    extraction output straight through.

    image_path is passed separately since run_pipeline() consumes the
    uploaded file but doesn't return the path in its output dict.
    """
    bridged_input = {
        "extracted_text": extraction_output.get("text", "") or "",
        "urls": extraction_output.get("urls", []) or [],
        "claimed_organization": extraction_output.get("claimed_organization") or None,
        "image_path": image_path,
    }

    return analyze(bridged_input)


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
    print("FULL PIPELINE RESULT (via analyze())")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # ---- Also test the adapter, using pipeline_service's exact output shape ----
    sample_extraction_output = {
        "input_type": "text",
        "text": "URGENT! Your account will be blocked. Verify your password now!!!",
        "urls": ["http://abc-bank-1ogin.xyz/verify"],
        "claimed_organization": "ABC Bank",
        "entities": {"phone_numbers": [], "emails": []},
    }

    adapter_result = analyze_from_extraction(sample_extraction_output)

    print("\n" + "=" * 60)
    print("FULL PIPELINE RESULT (via analyze_from_extraction() - Member 2's entry point)")
    print("=" * 60)
    print(json.dumps(adapter_result, indent=2, ensure_ascii=False))