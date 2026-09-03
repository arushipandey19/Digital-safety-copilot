from app.services.pipeline_service import run_pipeline

result = run_pipeline(
    input_type="text",
    text="""
    Your account has been suspended.
    Visit https://secure-account-check.com
    Contact support@banksecurity.com
    Call +91 9876543210
    """
)

print("PIPELINE RESULT:")
print(result)