from app.services.entity_extractor import extract_entities

text = """
Your account has been suspended.
Contact Bank Security at support@banksecurity.com
or call +91 9876543210.
"""

result = extract_entities(text)

print("EXTRACTED ENTITIES:")
print(result)