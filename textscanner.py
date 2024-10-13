from bs4 import BeautifulSoup
import re
from utils.contrast_utils import contrast_ratio, hex_to_rgb, css_to_hex
from utils.css_parser import parse_css
from utils.html_utils import parse_html, get_computed_style, has_direct_contents, get_background_color
from utils.debug import debug_print

# Accessibility constants
NORMAL_TEXT_SIZE_PX = 16
LARGE_TEXT_SIZE_PX = 18
BOLD_LARGE_TEXT_SIZE_PX = 14
MIN_FONT_WEIGHT_BOLD = 700

DEBUG = False
TAGS_TO_SKIP = ["html", "title", "head", "style", "script"]

def score_text_accessibility(html_content, css_content):
    """Scores the text accessibility based on font size and weight."""
    num_elements = 0
    num_accessible = 0

    # Parse HTML and CSS content
    soup = BeautifulSoup(html_content, "html.parser")
    styles = parse_css(css_content)

    for element in soup.find_all(True):
        if element.name in TAGS_TO_SKIP:
            continue

        num_elements += 1
        elem_style = get_computed_style(element, styles)

        # Get font size and weight from CSS
        font_size = elem_style.get("font-size", "16px")
        font_weight = int(elem_style.get("font-weight", "400"))

        # Check if the text is accessible based on size/weight
        if is_text_accessible(font_size, font_weight):
            num_accessible += 1

        debug_print(
            f"Element: {element.name}, Font Size: {font_size}, Font Weight: {font_weight}"
        )

    # Calculate accessibility score
    if num_elements == 0:
        return 100

    text_score = (num_accessible / num_elements) * 100
    return round(text_score, 1)


def is_text_accessible(font_size: str, font_weight: int) -> bool:
    """Checks if the text size and weight comply with WCAG accessibility guidelines."""
    font_size_value = int(re.match(r"\d+", font_size).group())

    # Check if it's large text or bold large text
    if font_size_value >= LARGE_TEXT_SIZE_PX or (font_weight >= MIN_FONT_WEIGHT_BOLD and font_size_value >= BOLD_LARGE_TEXT_SIZE_PX):
        return True

    # Check if it's normal size and at least 16px
    return font_size_value >= NORMAL_TEXT_SIZE_PX


if __name__ == "__main__":
    """Example usage of text accessibility scanner."""
    html_content = """
    <html>
    <head><style>p { font-size: 20px; }</style></head>
    <body>
        <p class="normal">This is a paragraph.</p>
        <h1>This is a heading</h1>
        <p style="font-size: 12px;">Small text here.</p>
    </body>
    </html>
    """
    css_content = """
    p {
        font-size: 16px;
        font-weight: 400;
    }
    h1 {
        font-size: 32px;
        font-weight: 700;
    }
    """

    text_score = score_text_accessibility(html_content, css_content)
    print(f"Text Accessibility Score: {text_score}%")
