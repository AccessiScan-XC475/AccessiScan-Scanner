"""
Module to calculate text accessibility scores based on 
font sizes and weights as per WCAG guidelines.
"""
import sys
import math

from utils.text_computations import compute_font_size
from utils.common_utils import parse_and_iterate_elements
from services.html_parser import get_computed_style

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
    Scores the accessibility of text elements based on font size and weight.
    Uses WCAG criteria to determine if text elements are accessible for
    users with visual impairments.
    """
    def handle_element(element, styles):
        """
        Evaluates a single HTML element for text accessibility based on
        font size and weight criteria defined by WCAG guidelines.
        """
        elem_style = get_computed_style(element, styles)
        font_size_val = compute_font_size(elem_style, element.name)
        font_weight = elem_style.get("font-weight", "400")
        try:
            font_weight = int(font_weight)
        except ValueError:
            font_weight = 400

        # Accessibility logic for font size and weight
        if font_size_val >= LARGE_TEXT_SIZE_PX:
            return True
        if font_size_val >= NORMAL_TEXT_SIZE_PX and font_weight >= NORM_FONT_WEIGHT:
            return True
        if font_size_val >= BOLD_LARGE_TEXT_SIZE_PX and font_weight >= MIN_FONT_WEIGHT_BOLD:
            return True
        return False

    num_elements, num_accessible, inaccessible_elements = parse_and_iterate_elements(
        html_content, css_content, TAGS_TO_SKIP, handle_element
    )

    if num_elements == 0:
        return 100  # Default score if no elements are found

    score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [score, inaccessible_elements]
