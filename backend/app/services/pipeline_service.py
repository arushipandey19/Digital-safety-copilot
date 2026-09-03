from app.services.ocr_service import extract_text_from_image
from app.services.url_extractor import extract_urls
from app.services.entity_extractor import extract_entities


def run_pipeline(input_type, text="", image_path=None, url=""):
    extracted_text = text

    if input_type == "screenshot":
        if not image_path:
            raise ValueError("Image path is required for screenshot input")

        extracted_text = extract_text_from_image(image_path)

    urls = extract_urls(extracted_text)

    if url and url not in urls:
        urls.append(url)

    entities = extract_entities(extracted_text)

    return {
        "input_type": input_type,
        "text": extracted_text,
        "urls": urls,
        "claimed_organization": entities["claimed_organization"],
        "entities": {
            "phone_numbers": entities["phone_numbers"],
            "emails": entities["emails"]
        }
    }