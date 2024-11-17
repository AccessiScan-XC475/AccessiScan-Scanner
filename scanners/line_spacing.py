"""Module to evaluate line spacing for accessibility."""
import math
from utils.debug import debug_print
from services.css_parser import parse_css
from services.html_parser import parse_html, get_computed_style, has_direct_contents
from scanners.text_scanner import compute_font_size

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
    num_elements = 0
    num_accessible = 0
    inaccessible_elements = []

    soup = parse_html(html_content)
    styles = parse_css(css_content)

    for element in soup.find_all(True):
        if element.hidden or element.name in TAGS_TO_SKIP or not has_direct_contents(element):
            continue

        num_elements += 1
        elem_style = get_computed_style(element, styles)
        debug_print(element, elem_style)

        # Compute font size and line height
        font_size_val = compute_font_size(elem_style, element.name)
        line_height_val = compute_line_height(elem_style, font_size_val)

        # Determine if line height meets accessibility ratio
        required_ratio = HEADER_TEXT_RATIO if element.name in HEADER_TAGS else BODY_TEXT_RATIO
        line_spacing_ratio = line_height_val / font_size_val
        is_accessible = line_spacing_ratio >= required_ratio

        # Update accessibility counts
        if is_accessible:
            num_accessible += 1
        else:
            inaccessible_elements.append(element)

        # Debug print for element details
        print(f"Element: {element.name}, Font Size: {font_size_val}px, "
              f"Line Height: {line_height_val}px, Line Spacing Ratio: {line_spacing_ratio:.2f}, "
              f"Is Accessible: {is_accessible}")

    if num_elements == 0:
        return 100

    trunc_score = math.floor((num_accessible / num_elements) * 1000) / 10
    return [trunc_score, inaccessible_elements]

def compute_line_height(elem_style, font_size_val):
    """
    Compute line height based on element style or default ratio.
    """
    line_height = elem_style.get("line-height", "normal")
    if line_height == "normal":
        return 1.5 * font_size_val
    try:
        return float(line_height) * font_size_val
    except ValueError:
        return compute_font_size({"font-size": line_height}, "")
