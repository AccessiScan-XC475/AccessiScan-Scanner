"""
Module to calculate text accessibility scores based on 
font sizes and weights as per WCAG guidelines.
"""
import sys
import math
from utils.debug import debug_print
from utils.text_computations import compute_font_size
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

    # Parse the HTML and CSS content
    soup = parse_html(html_content)
    styles = parse_css(css_content)

    # Iterate over all elements in the HTML content
    for element in soup.find_all(True):
        if element.hidden or element.name in TAGS_TO_SKIP or not has_direct_contents(element):
            continue  # Skip elements that are hidden or in the skip list

        num_elements += 1
        elem_style = get_computed_style(element, styles)
        debug_print(element, elem_style)

        # Compute the font size using the imported utility function
        font_size_val = compute_font_size(elem_style, element.name)

        # Determine the font weight and handle any invalid values gracefully
        font_weight = elem_style.get("font-weight", "400")
        try:
            font_weight = int(font_weight)
        except ValueError:
            font_weight = 400  # Default font weight if not a valid integer

        # Determine if the text is accessible based on font size and weight criteria
        if font_size_val >= LARGE_TEXT_SIZE_PX:
            is_accessible = True
        elif font_size_val >= NORMAL_TEXT_SIZE_PX and font_weight >= NORM_FONT_WEIGHT:
            is_accessible = True
        elif font_size_val >= BOLD_LARGE_TEXT_SIZE_PX and font_weight >= MIN_FONT_WEIGHT_BOLD:
            is_accessible = True
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

    # Calculate and return the accessibility score
    if num_elements == 0:
        return 100  # Default score if no elements are found

    score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [score, inaccessible_elements]
