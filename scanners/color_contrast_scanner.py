import math
import itertools
from utils.contrast_utils import contrast_ratio, hex_to_rgb, css_to_hex
from utils.debug import debug_print
from utils.common_utils import parse_and_iterate_elements  # Use the shared function
from services.html_parser import get_computed_style

NORMAL_TEXT_CONTRAST_RATIO = 4.5
OTHER_CONTRACT_RATIO = 3
TAGS_TO_SKIP = ["html", "title", "head", "style", "script", "body"]

def score_text_contrast(html_content, css_content):
    """
    Parses HTML and CSS content.
    Returns a score based on the percentage of text elements with
    adequate contrast between text and background colors.
    """
    def handle_element(element, styles):
        elem_style = get_computed_style(element, styles)
        debug_print(element, elem_style)
        # Get the text color and background color
        color = css_to_hex(elem_style.get("color", ""))
        background_color = css_to_hex(elem_style.get("background-color", ""))
        # Convert colors to RGB values
        color_rgb = hex_to_rgb(color if color is not None else "#000000")
        bg_rgb = hex_to_rgb(background_color if background_color is not None else "#FFFFFF")
        # Calculate the contrast ratio
        ratio = contrast_ratio(color_rgb, bg_rgb)
        is_accessible = ratio >= NORMAL_TEXT_CONTRAST_RATIO

        # Debug print for each element's contrast details
        print(
            f"Element: {element.name}, Text Color: {color}, "
            f"Background Color: {background_color}, Contrast Ratio: {ratio:.2f}, "
            f"Is Accessible: {is_accessible}"
        )

        return is_accessible

    num_elements, num_accessible, inaccessible_elements = parse_and_iterate_elements(
        html_content, css_content, TAGS_TO_SKIP, handle_element
    )

    if num_elements == 0:
        return 100  # Default score if no elements are found

    trunc_score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [trunc_score, inaccessible_elements]
