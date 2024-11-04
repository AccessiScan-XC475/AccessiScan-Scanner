"""
Module to check image accessibility based on the presence of alt text in both HTML and CSS.
"""

import sys
from bs4 import BeautifulSoup
import re

if __name__ == "__main__":
    # configure python path to root of project
    path = "/".join(sys.path[0].split("/")[:-1])
    sys.path[0] = path

from services.html_parser import parse_html
from utils.debug import debug_print


def score_image_accessibility(html, css=None):
    """
    Parses HTML content and optionally CSS content.
    Returns the number of images with alt text and the total number of images.
    """
    total_images = 0
    images_with_alt = 0
    images_without_alt = []

    soup = parse_html(html)

    # CSS can affect alt attributes if set as pseudo-elements; this is rare but possible.
    # If CSS is provided, we check for attributes related to alt content.
    css_alt_patterns = []
    if css:
        css_alt_patterns = re.findall(r'img\[alt[^\]]*="([^"]*)"\]', css)
    
    # Analyze each image element in the HTML
    for img_element in soup.find_all("img"):
        total_images += 1
        alt_text = img_element.get("alt", "").strip()

        # Fallback to CSS-defined alt attribute if HTML alt is missing
        if not alt_text and css_alt_patterns:
            for pattern in css_alt_patterns:
                if pattern in img_element.get("src", ""):
                    alt_text = pattern
                    break

        if alt_text:  # If alt text is present
            images_with_alt += 1
        else:  # If alt text is missing
            images_without_alt.append(img_element)

        debug_print(
            f"Image: {img_element.get('src', 'No src')}, Alt Text: {'Present' if alt_text else 'Missing'}"
        )

    if total_images == 0:
        return "No images on the page"

    return {
        "images_with_alt": images_with_alt,
        "total_images": total_images,
        "score": (images_with_alt / total_images)
    }


if __name__ == "__main__":
    # Example usage
    SAMPLE_HTML = """
    <html>
    <head></head>
    <body>
        <img src="image1.jpg" alt="A descriptive text for image 1.">
        <img src="image2.jpg" alt="">
        <img src="image3.jpg">
        <img src="image4.jpg" alt="A descriptive text for image 4.">
    </body>
    </html>
    """
    SAMPLE_CSS = """
    img[alt="Image from CSS"] {
        content: "Alternative text from CSS";
    }
    """

    image_accessibility_score = score_image_accessibility(SAMPLE_HTML, SAMPLE_CSS)
    if isinstance(image_accessibility_score, str):
        print(image_accessibility_score)
    else:
        print(
            f"Images with Alt Text: {image_accessibility_score['images_with_alt']} / Total Images: {image_accessibility_score['total_images']}"
        )
        print(f"Image Accessibility Score: {image_accessibility_score['score']}")
