import sys
import os
import re
import cv2
import json

# Route extracted URLs through the RULE-BASED analyzer, not ML.
# security_engine/url/url_analyser.py lives two folders over from here
# (ml_engine/qr.py -> ../security_engine/url/url_analyser.py)
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "security_engine", "url")
)
from url_analyser import analyze_urls


def extract_qr_data(image_path: str) -> list:
    """
    Detect and decode QR codes from an image.
    (Unchanged - this part was never ML, purely OpenCV detection.)
    """

    img = cv2.imread(image_path)

    if img is None:
        return [{
            "error": f"Could not open image: {image_path}"
        }]

    detector = cv2.QRCodeDetector()
    results = []

    # ---------------------------------------------------------
    # Try multiple QR codes
    # ---------------------------------------------------------
    try:
        success, decoded_info, points, _ = detector.detectAndDecodeMulti(img)

        if success and decoded_info:

            for i, data in enumerate(decoded_info):

                if not data:
                    continue

                data = data.strip()

                is_url = bool(
                    re.match(
                        r"^(https?://|www\.)",
                        data,
                        re.IGNORECASE
                    )
                )

                position = None

                if points is not None and i < len(points):

                    pts = points[i]

                    x_min = int(pts[:, 0].min())
                    y_min = int(pts[:, 1].min())
                    x_max = int(pts[:, 0].max())
                    y_max = int(pts[:, 1].max())

                    position = {
                        "left": x_min,
                        "top": y_min,
                        "width": x_max - x_min,
                        "height": y_max - y_min
                    }

                results.append({
                    "raw_data": data,
                    "is_url": is_url,
                    "qr_type": "QRCODE",
                    "position": position
                })

    except Exception as e:
        print(f"Multi-QR detection failed: {e}")

    # ---------------------------------------------------------
    # Fallback: single QR code
    # ---------------------------------------------------------
    if not results:

        try:
            data, points, _ = detector.detectAndDecode(img)

            if data:

                data = data.strip()

                is_url = bool(
                    re.match(
                        r"^(https?://|www\.)",
                        data,
                        re.IGNORECASE
                    )
                )

                position = None

                if points is not None:

                    pts = points[0]

                    x_min = int(pts[:, 0].min())
                    y_min = int(pts[:, 1].min())
                    x_max = int(pts[:, 0].max())
                    y_max = int(pts[:, 1].max())

                    position = {
                        "left": x_min,
                        "top": y_min,
                        "width": x_max - x_min,
                        "height": y_max - y_min
                    }

                results.append({
                    "raw_data": data,
                    "is_url": is_url,
                    "qr_type": "QRCODE",
                    "position": position
                })

        except Exception as e:
            print(f"Single QR detection failed: {e}")

    return results


def analyze_screenshot_qr(image_path: str, claimed_organization: str = None) -> dict:
    """
    Detect QR codes and send extracted URLs to the RULE-BASED
    security_engine URL analyzer (not ML - that classifier was removed).

    claimed_organization: optional - pass this through if the message
    text (from OCR, extracted separately) names an organization, so
    domain-mismatch checking can work. Defaults to None if unknown.
    """

    qr_results = extract_qr_data(image_path)

    # ---------------------------------------------------------
    # Handle image error
    # ---------------------------------------------------------
    if (
        len(qr_results) == 1
        and "error" in qr_results[0]
    ):
        return {
            "qr_codes_found": 0,
            "qr_data": [],
            "extracted_urls": [],
            "url_analysis": {},
            "error": qr_results[0]["error"]
        }

    valid_results = [
        result
        for result in qr_results
        if "raw_data" in result
    ]

    extracted_urls = [
        result["raw_data"]
        for result in valid_results
        if result.get("is_url")
    ]

    # ---------------------------------------------------------
    # Send every extracted URL to the RULE-BASED analyzer as a batch
    # (analyze_urls handles the empty-list case gracefully too)
    # ---------------------------------------------------------
    url_analysis = analyze_urls(extracted_urls, claimed_organization)

    return {
        "qr_codes_found": len(valid_results),
        "qr_data": valid_results,
        "extracted_urls": extracted_urls,
        "url_analysis": url_analysis
    }


# =============================================================
# Command-line execution
# =============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Usage:")
        print("    python qr.py <path_to_screenshot> [claimed_organization]")

        print("\nExample:")
        print("    python qr.py qrimage.jpeg")
        print('    python qr.py qrimage.jpeg "SBI"')

        sys.exit(1)

    image_path = sys.argv[1]
    claimed_org = sys.argv[2] if len(sys.argv) > 2 else None

    result = analyze_screenshot_qr(image_path, claimed_org)

    print()
    print("=" * 60)
    print("QR CODE ANALYSIS")
    print("=" * 60)

    print(f"\nQR codes found: {result['qr_codes_found']}")

    for i, qr in enumerate(result["qr_data"], start=1):
        print(f"\nQR Code #{i}")
        print("-" * 40)
        print(f"Type     : {qr.get('qr_type')}")
        print(f"Data     : {qr.get('raw_data')}")
        print(f"Is URL   : {qr.get('is_url')}")
        print(f"Position : {qr.get('position')}")

    if result["extracted_urls"]:
        print()
        print("=" * 60)
        print("RULE-BASED URL ANALYSIS")
        print("=" * 60)
        print(json.dumps(result["url_analysis"], indent=2))
    else:
        print("\nNo URLs found in any QR code.")

    print()