from app.services.url_extractor import extract_urls

text = """
Your account needs verification.
Visit https://secure-account-check.com immediately.
"""

urls = extract_urls(text)

print("EXTRACTED URLS:")
print(urls)