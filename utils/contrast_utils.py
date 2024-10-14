"""
Utility module for handling color conversions and calculating contrast ratios
according to WCAG accessibility guidelines.
"""
import math
import re
from PIL import ImageColor
from utils.debug import debug_print

def css_to_hex(color):
    """
    Converts a CSS color into a hex value.
    """
    # Check if it's a valid hex value
    if bool(re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color)):
        return color

    # Check if it's a valid string rgb tuple
    rgb_match = re.match(
        r"^\s*rgb\s*\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)\s*$",
        color,
        re.IGNORECASE,
    )
    if rgb_match:
        # Get rgb values
        r, g, b = map(int, rgb_match.groups())

        # Check all rgb values are valid
        if all(0 <= x <= 255 for x in (r, g, b)):
            return rgb_to_hex((r, g, b))

    # Try to convert css color word (e.g., 'red') to hex
    try:
        rgb = ImageColor.getrgb(color)
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    except ValueError:
        return None


def rgb_to_hex(rgb):
    """
    Converts an rgb tuple or list to its hex string.
    Assumes valid rgb input
    """
    r, g, b = list(rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(hex_color):
    """
    Converts a hexcode color into an rgb tuple.
    Assumes valid hex input
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        return tuple(int(hex_color[i] + hex_color[1], 16) for i in range(3))
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def calculate_luminance(rgb: tuple[int, ...]):
    """
    Calculates the apparent lumunicance of the input color.
    Assumes color is rgb tuple with min 0 and max 255
    """

    def conv(color):
        i = float(color) / 255
        if i < 0.03928:
            return i / 12.92
        return ((i + 0.055) / 1.055) ** 2.4

    # https://www.w3.org/TR/WCAG20/#relativeluminancedef
    # Calculate relative luminance
    r, g, b = [conv(x) for x in rgb]

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1: tuple[int, ...], rgb2: tuple[int, ...]):
    """
    Returns the contrast ratio between two colors truncated to the hundreths place
    """
    l_1 = calculate_luminance(rgb1)
    l_2 = calculate_luminance(rgb2)

    lighter = max(l_1, l_2)
    darker = min(l_1, l_2)

    debug_print(lighter, darker)

    # https://www.accessibility-developer-guide.com/knowledge/colours-and-contrast/how-to-calculate/
    ratio = (lighter + 0.05) / (darker + 0.05)
    return math.floor(ratio * 100) / 100.0
