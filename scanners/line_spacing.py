"""Module to evaluate line spacing for accessibility."""
import math
from utils.debug import debug_print
from services.css_parser import parse_css
from services.html_parser import parse_html, get_computed_style, has_direct_contents

BODY_TEXT_RATIO = 1.5
HEADER_TEXT_RATIO = 1.2
TAGS_TO_SKIP = ["html", "title", "head", "style", "script", "body"]
HEADER_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]

def compute_font_size(text_elem_style, element_tag, root_font_size=16):
    """
    Compute font size accurately, handling rem, em, and px.
    """
    font_size = text_elem_style.get("font-size", "16px")

    # Handle specific elements with default em sizes
    if element_tag == "button":
        return 0.83 * root_font_size
    if element_tag == "h1":
        return 2 * root_font_size
    if element_tag == "h3":
        return 1.17 * root_font_size

    # Handle other cases (rem, em, and px)
    if "rem" in font_size:
        return float(font_size.replace("rem", "")) * root_font_size
    elif "em" in font_size:
        return float(font_size.replace("em", "")) * root_font_size
    elif "px" in font_size:
        return float(font_size.replace("px", ""))
    elif "pt" in font_size:
        return float(font_size.replace("pt", "")) * 1.33  # Convert pt to px
    else:
        return float(font_size)

def score_line_spacing(html_content, css_content):
    """
    Parses HTML and CSS content.
    Returns a score based on the percentage of text elements with
    adequate line spacing according to WCAG standards.
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

        line_height = elem_style.get("line-height", "normal")
        if line_height == "normal":
        # Use a typical default ratio for line height when not explicitly specified
            line_height_val = 1.5 * font_size_val  
        else:
        # Check if line height is a multiplier (e.g., '3' with no units)
            try:
                line_height_val = float(line_height) * font_size_val
            except ValueError:
        # If line height has units, convert using existing logic
                line_height_val = compute_font_size({"font-size": line_height}, element.name)

        # Ensure that the line height is at least 1.2 times the font size for reasonable spacing
        if line_height_val < font_size_val * 1.2:
            line_height_val = 1.2 * font_size_val

        # Determine the required ratio
        required_ratio = HEADER_TEXT_RATIO if element.name in HEADER_TAGS else BODY_TEXT_RATIO

        # Calculate the line spacing ratio
        line_spacing_ratio = line_height_val / font_size_val
        is_accessible = line_spacing_ratio >= required_ratio

        if is_accessible:
            num_accessible += 1
        else:
            inaccessible_elements.append(element)

        # Debug print for each element's line spacing details
        print(
            f"Element: {element.name}, Font Size: {font_size_val}px, "
            f"Line Height: {line_height_val}px, Line Spacing Ratio: {line_spacing_ratio:.2f}, "
            f"Is Accessible: {is_accessible}"
        )

    if num_elements == 0:
        return 100

    trunc_score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [trunc_score, inaccessible_elements]