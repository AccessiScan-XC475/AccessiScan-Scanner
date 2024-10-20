"""Module to calculate text contrast scores for accessibility."""
import math
import re
from utils.debug import debug_print
from services.css_parser import parse_css
from services.html_parser import parse_html, get_computed_style

NORMAL_TEXT_SIZE_PX = 16
LARGE_TEXT_SIZE_PX = 18
BOLD_LARGE_TEXT_SIZE_PX = 14
MIN_FONT_WEIGHT_BOLD = 700

TAGS_TO_SKIP = ["html", "title", "head", "style", "script"]

def score_text_accessibility(html, css):
    """
    Parses HTML and CSS content.
    Returns a score based on percentage of text elements with
    adequate contrast between text and background colors
    """
    text_num_elements = 0
    text_num_accessible = 0
    text_accessible_elements = []
    text_inaccessible_elements = []

    soup = parse_html(html)
    styles = parse_css(css)

    for text_element in soup.find_all(True):
        if (
            text_element.hidden
            or text_element.name in TAGS_TO_SKIP
            or not text_element.get_text(strip=True)
        ):
            continue

        text_num_elements += 1
        text_elem_style = get_computed_style(text_element, styles)
        debug_print(text_element, text_elem_style)

        # Get font size and weight from CSS
        font_size = text_elem_style.get("font-size", "16px")
        font_weight = int(text_elem_style.get("font-weight", "400"))

        # Check if the text is accessible based on size/weight
        if is_text_accessible(font_size, font_weight):
            text_num_accessible += 1
            text_accessible_elements.append(text_element)
        else:
            # Log only if it's a text-related issue
            text_inaccessible_elements.append(text_element)

        debug_print(
            f"Element: {text_element.name}, Font Size: {font_size}, Font Weight: {font_weight}"
        )

    if text_num_elements == 0:
        return 100

    text_score = (text_num_accessible / text_num_elements) * 100
    trunc_score = math.floor(text_score * 10) / 10
    debug_print(text_num_accessible, text_num_elements, trunc_score)
    return [trunc_score, text_accessible_elements, text_inaccessible_elements]

def is_text_accessible(font_size: str, font_weight: int) -> bool:
    """
    Checks if text is adequately sized.
    """
    font_size_value = int(re.match(r"\d+", font_size).group())

    # Check if it's large text or bold large text
    if font_size_value >= LARGE_TEXT_SIZE_PX or (
        font_weight >= MIN_FONT_WEIGHT_BOLD and font_size_value >= BOLD_LARGE_TEXT_SIZE_PX
    ):
        return True

    # Check if it's normal text size and at least 16px
    return font_size_value >= NORMAL_TEXT_SIZE_PX

if __name__ == "__main__":
    # Example usage
    SAMPLE_HTML = """
    <html>
    <head><style>p { font-size: 20px; }</style></head>
    <body>
        <p class="normal">This is a paragraph.</p>
        <h1>This is a heading</h1>
        <p style="font-size: 12px;">Small text here.</p>
    </body>
    </html>
    """
    SAMPLE_CSS = """
    p {
        font-size: 16px;
        font-weight: 400;
    }
    h1 {
        font-size: 32px;
        font-weight: 700;
    }
    """

    text_accessibility_score = score_text_accessibility(SAMPLE_HTML, SAMPLE_CSS)
    print(f"Text Accessibility Score: {text_accessibility_score}%")
