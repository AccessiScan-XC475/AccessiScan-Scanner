"""
Module to check image accessibility based on the presence of alt text.
"""
import math
from services.html_parser import parse_html
from utils.debug import debug_print

def score_image_accessibility(html):
    """
    Parses HTML content.
    Returns the number of images with alt text and the total number of images.
    """
    total_images = 0
    images_with_alt = 0
    images_without_alt = []

    soup = parse_html(html)

    for img_element in soup.find_all('img'):
        total_images += 1
        
        # Check for the presence of alt text
        alt_text = img_element.get('alt', '').strip()
        
        if alt_text:  # If alt text is present
            images_with_alt += 1
        else:  # If alt text is missing
            images_without_alt.append(img_element)

        debug_print(
            f"Image: {img_element['src']}, Alt Text: {'Present' if alt_text else 'Missing'}"
        )

    if total_images == 0:
        return "No images on the page"

    return {
        "images_with_alt": images_with_alt,
        "total_images": total_images,
    "score": math.floor((images_with_alt / total_images) * 1000) / 10,
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

    image_accessibility_score = score_image_accessibility(SAMPLE_HTML)
    if isinstance(image_accessibility_score, str):
        print(image_accessibility_score)
    else:
        print(f"Images with Alt Text: {image_accessibility_score['images_with_alt']} / Total Images: {image_accessibility_score['total_images']}")
        print(f"Image Accessibility Score: {image_accessibility_score['score']}")
