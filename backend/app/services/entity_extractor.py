import re

def extract_emails(text: str):
    if not text:
        return []

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    return list(dict.fromkeys(re.findall(pattern, text)))


def extract_phone_numbers(text: str):
    if not text:
        return []

    pattern = r'(?<!\d)\+?\d[\d\s().-]{8,}\d(?!\d)'

    numbers = re.findall(pattern, text)

    cleaned = []

    for number in numbers:
        number = re.sub(r'\s+', ' ', number).strip()

        if number not in cleaned:
            cleaned.append(number)

    return cleaned


def extract_organization(text: str):
    if not text:
        return ""

    patterns = [
        r'\b([A-Z][A-Za-z&]+(?:\s+[A-Z][A-Za-z&]+){0,3}\s+(?:Bank|Pay|Finance|Insurance|Airlines|Courier|Express|Delivery))\b',
        r'\b([A-Z][A-Za-z&]+(?:\s+[A-Z][A-Za-z&]+){0,2}\s+(?:Ltd|Limited|Inc|Corporation|Corp))\b'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(1)

    return ""


def extract_entities(text: str):
    return {
        "phone_numbers": extract_phone_numbers(text),
        "emails": extract_emails(text),
        "claimed_organization": extract_organization(text)
    }