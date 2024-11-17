"""
Calculates font size and line height.
"""
def compute_font_size(text_elem_style, element_tag, root_font_size=16):
    """
    This module contains utility functions for text-related computations, 
    including font size calculation and parsing styles for accessibility checks.
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
