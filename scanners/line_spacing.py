"""
Module to evaluate line spacing for accessibility.
"""
import math
from utils.debug import debug_print
from utils.text_computations import compute_font_size, compute_line_height
from utils.common_utils import parse_and_iterate_elements  # Import shared utility function
from services.html_parser import get_computed_style
from utils.common_utils import parse_and_iterate_elements  # Import shared utility function

BODY_TEXT_RATIO = 1.5
HEADER_TEXT_RATIO = 1.2
TAGS_TO_SKIP = ["html", "title", "head", "style", "script", "body"]
HEADER_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]

def score_line_spacing(html_content, css_content):
    """
    Parses HTML and CSS content.
    Returns a score based on the percentage of text elements with
    adequate line spacing according to WCAG standards.
    """
    def handle_element(element, styles):
        """
        Handle each element by evaluating its line spacing accessibility.
        """
        elem_style = get_computed_style(element, styles)
        debug_print(element, elem_style)

        # Compute font size and line height
        font_size_val = compute_font_size(elem_style, element.name)
        line_height_val = compute_line_height(elem_style, font_size_val)

        # Determine if line height meets accessibility ratio
        required_ratio = HEADER_TEXT_RATIO if element.name in HEADER_TAGS else BODY_TEXT_RATIO
        line_spacing_ratio = line_height_val / font_size_val
        is_accessible = line_spacing_ratio >= required_ratio

        # Debug print for element details
        print(f"Element: {element.name}, Font Size: {font_size_val}px, "
              f"Line Height: {line_height_val}px, Line Spacing Ratio: {line_spacing_ratio:.2f}, "
              f"Is Accessible: {is_accessible}")

        return is_accessible

    num_elements, num_accessible, inaccessible_elements = parse_and_iterate_elements(
        html_content, css_content, TAGS_TO_SKIP, handle_element
    )

    if num_elements == 0:
        return 100

    trunc_score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [trunc_score, inaccessible_elements]
