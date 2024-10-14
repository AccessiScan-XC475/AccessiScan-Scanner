"""
Module to calculate text accessibility scores based on font sizes and weights as per WCAG guidelines.
"""
import math
import re
from utils.css_parser import parse_css
from utils.html_utils import parse_html, get_computed_style
from utils.debug import debug_print

NORMAL_TEXT_SIZE_PX = 16
LARGE_TEXT_SIZE_PX = 18
BOLD_LARGE_TEXT_SIZE_PX = 14
MIN_FONT_WEIGHT_BOLD = 700

TAGS_TO_SKIP = ["html", "title", "head", "style", "script"]

def score_text_accessibility(html, css):
    """
    Parses HTML and CSS content.
    Returns a score based on the percentage of text elements with
    accessible font sizes and font weights as per WCAG guidelines.
    """
    
    num_elements = 0
    num_accessible = 0

    # Create an HTML parser from HTML content / DOM
    soup = parse_html(html)
    styles = parse_css(css)

    # Iterate through all elements in the HTML
    for element in soup.find_all(True):
        if (
            element.hidden
            or element.name in TAGS_TO_SKIP
            or not element.get_text(strip=True)  # Skipping elements without visible text
        ):
            continue

        num_elements += 1
        elem_style = get_computed_style(element, styles)
        debug_print(element, elem_style)

        # Get font size and weight from CSS
        font_size = elem_style.get("font-size", "16px")
        font_weight = int(elem_style.get("font-weight", "400"))

        # Check if the text is accessible based on size/weight
        if is_text_accessible(font_size, font_weight):
            num_accessible += 1

        # Debug print for each element's text accessibility details
        debug_print(
            f"Element: {element.name}, Font Size: {font_size}, Font Weight: {font_weight}"
        )

    # Avoid dividing by zero; if no elements, assume fully accessible
    if num_elements == 0:
        return 100

    # Calculate the score as a percentage of accessible elements
    text_score = (num_accessible / num_elements) * 100
    trunc_score = math.floor(text_score * 10) / 10  # Truncate to tenths for consistent scoring
    debug_print(num_accessible, num_elements, trunc_score)
    
    return trunc_score

def is_text_accessible(font_size: str, font_weight: int) -> bool:
    """
    Checks if the text size and weight comply with WCAG accessibility guidelines.
    """
    font_size_value = int(re.match(r"\d+", font_size).group())

    # Check if it's large text or bold large text
    if font_size_value >= LARGE_TEXT_SIZE_PX or (font_weight >= MIN_FONT_WEIGHT_BOLD and font_size_value >= BOLD_LARGE_TEXT_SIZE_PX):
        return True

    # Check if it's normal text size and at least 16px
    return font_size_value >= NORMAL_TEXT_SIZE_PX


if __name__ == "__main__":
    # Example usage of text accessibility scanner.
    # Sample HTML and CSS content
    sample_html = """
    <html>
    <head><style>p { font-size: 20px; }</style></head>
    <body>
        <p class="normal">This is a paragraph.</p>
        <h1>This is a heading</h1>
        <p style="font-size: 12px;">Small text here.</p>
    </body>
    </html>
    """
    sample_css = """
    p {
        font-size: 16px;
        font-weight: 400;
    }
    h1 {
        font-size: 32px;
        font-weight: 700;
    }
    """

    # Calculate text accessibility score
    text_accessibility_score = score_text_accessibility(sample_html, sample_css)
    print(f"Text Accessibility Score: {text_accessibility_score}%")
