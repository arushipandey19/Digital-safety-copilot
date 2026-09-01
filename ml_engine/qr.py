"""
QR Code Extractor for Screenshots
----------------------------------
Detects and decodes QR codes from screenshots using OpenCV.

If a QR code contains a URL:
    1. Extract the URL
    2. Send it directly to the existing URL ML classifier
    3. Return the phishing probability

Usage:
    python qr.py qrimage.jpeg
"""

import sys
import re
import cv2

# Import your existing URL ML classifier
from url import predict_single_url


def extract_qr_data(image_path: str) -> list:
    """
    Detect and decode QR codes from an image.
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


def analyze_screenshot_qr(image_path: str) -> dict:
    """
    Detect QR codes and send extracted URLs to the
    existing URL ML classifier.
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
            "url_analysis": [],
            "error": qr_results[0]["error"]
        }

    valid_results = [
        result
        for result in qr_results
        if "raw_data" in result
    ]

    extracted_urls = []
    url_analysis = []

    # ---------------------------------------------------------
    # Send every extracted URL to existing ML model
    # ---------------------------------------------------------
    for result in valid_results:

        if result.get("is_url"):

            url = result["raw_data"]

            extracted_urls.append(url)

            try:

                prediction = predict_single_url(url)

                result["ml_prediction"] = prediction

                url_analysis.append(prediction)

            except Exception as e:

                result["ml_prediction_error"] = str(e)

                url_analysis.append({
                    "url": url,
                    "error": str(e)
                })

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
        print("    python qr.py <path_to_screenshot>")

        print("\nExample:")
        print("    python qr.py qrimage.jpeg")

        sys.exit(1)

    image_path = sys.argv[1]

    result = analyze_screenshot_qr(image_path)

    print()
    print("=" * 60)
    print("QR CODE ANALYSIS")
    print("=" * 60)

    print(
        f"\nQR codes found: "
        f"{result['qr_codes_found']}"
    )

    # ---------------------------------------------------------
    # Display QR results
    # ---------------------------------------------------------

    for i, qr in enumerate(result["qr_data"], start=1):

        print(f"\nQR Code #{i}")
        print("-" * 40)

        print(f"Type     : {qr.get('qr_type')}")
        print(f"Data     : {qr.get('raw_data')}")
        print(f"Is URL   : {qr.get('is_url')}")
        print(f"Position : {qr.get('position')}")

        # -----------------------------------------------------
        # Display ML prediction
        # -----------------------------------------------------

        if "ml_prediction" in qr:

            prediction = qr["ml_prediction"]

            probability = prediction.get(
                "phishing_probability"
            )

            print("\nURL ML ANALYSIS")
            print("-" * 40)

            print(
                f"Phishing Probability : "
                f"{probability}"
            )

            # Simple interpretation
            if probability is not None:

                if probability >= 0.70:
                    risk = "HIGH RISK"

                elif probability >= 0.40:
                    risk = "SUSPICIOUS"

                else:
                    risk = "LOW RISK"

                print(f"Risk Level           : {risk}")

        elif "ml_prediction_error" in qr:

            print(
                "\nML Analysis Error: "
                f"{qr['ml_prediction_error']}"
            )

    # ---------------------------------------------------------
    # URLs
    # ---------------------------------------------------------

    if result["extracted_urls"]:

        print()
        print("=" * 60)
        print("EXTRACTED URLS")
        print("=" * 60)

        for url in result["extracted_urls"]:
            print(url)

    else:

        print("\nNo URLs found in any QR code.")

    print()