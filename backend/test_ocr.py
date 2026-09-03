from app.services.ocr_service import extract_text_from_image

image_path = "test_image.png"

text = extract_text_from_image(image_path)

print("EXTRACTED TEXT:")
print(text)