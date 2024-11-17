"""
Module to calculate text accessibility scores based on 
font sizes and weights as per WCAG guidelines.
"""
import sys
import math
from utils.debug import debug_print
from services.css_parser import parse_css
from services.html_parser import parse_html, get_computed_style, has_direct_contents

if __name__ == "__main__":
    # Configure python path to root of project
    PATH = "/".join(sys.path[0].split("/")[:-1])
    sys.path[0] = PATH  # Fixed sys.PATH to sys.path

NORMAL_TEXT_SIZE_PX = 16
LARGE_TEXT_SIZE_PX = 18
BOLD_LARGE_TEXT_SIZE_PX = 14
MIN_FONT_WEIGHT_BOLD = 700
NORM_FONT_WEIGHT = 400

TAGS_TO_SKIP = ["html", "title", "head", "style", "script",
                "div", "body", "header", "nav", "main"]

def score_text_accessibility(html_content, css_content):
    """
    Parses HTML and CSS content.
    Returns a score based on the percentage of text elements with
    adequate text size according to WCAG standards.
    """
    num_elements = 0
    num_accessible = 0
    inaccessible_elements = []

    soup = parse_html(html_content)
    styles = parse_css(css_content)

    for element in soup.find_all(True):
        if (
            element.hidden
            or element.name in TAGS_TO_SKIP
            or not has_direct_contents(element)
        ):
            continue
        num_elements += 1
        elem_style = get_computed_style(element, styles)
        debug_print(element, elem_style)

        # Compute the font size using the helper function
        font_size_val = compute_font_size(elem_style, element.name)

        # Check for bold styling
        font_weight = elem_style.get("font-weight", "400")
        try:
            font_weight = int(font_weight)
        except ValueError:
            font_weight = 400  # Default font weight

        # Determine accessibility criteria
        if font_size_val >= LARGE_TEXT_SIZE_PX:
            is_accessible = True
        elif font_size_val >= NORMAL_TEXT_SIZE_PX and font_weight >= NORM_FONT_WEIGHT:
            is_accessible = font_size_val >= NORMAL_TEXT_SIZE_PX
        elif font_size_val >= BOLD_LARGE_TEXT_SIZE_PX and font_weight >= MIN_FONT_WEIGHT_BOLD:
            is_accessible = font_size_val >= BOLD_LARGE_TEXT_SIZE_PX
        else:
            is_accessible = False

        if is_accessible:
            num_accessible += 1
        else:
            inaccessible_elements.append(element)

        # Debug print for each element's text size details
        print(
            f"Element: {element.name}, Font Size: {font_size_val}px, "
            f"Font Weight: {font_weight}, Is Accessible: {is_accessible}"
        )

    if num_elements == 0:
        return 100

    score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [score, inaccessible_elements]

def compute_font_size(text_elem_style, element_tag, root_font_size=16):
    """
    Compute font size accurately, handling rem, em, px, and specific HTML elements.
    """
    font_size = text_elem_style.get("font-size", "16px")

    # Handle specific elements with default em sizes
    default_sizes = {
        "button": 0.83 * root_font_size,
        "h1": 2 * root_font_size,
        "h3": 1.17 * root_font_size
    }
    if element_tag in default_sizes:
        return default_sizes[element_tag]

    # Handle font-size cases (rem, em, px, pt)
    units = [("rem", root_font_size), ("em", root_font_size), ("px", 1), ("pt", 1.33)]
    for unit, multiplier in units:
        if unit in font_size:
            return float(font_size.replace(unit, "")) * multiplier

    # Default case if no recognizable unit is found
    return float(font_size)

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
