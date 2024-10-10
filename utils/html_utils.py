
from bs4 import BeautifulSoup
from utils.contrast_utils import css_to_hex

def parse_html(html_content):
    # Parse HTML content and return the soup object
    return BeautifulSoup(html_content, "html.parser")

def get_computed_style(element, styles):
    elem_style = {}
    classes = ["." + x for x in element.attrs.get("class", [])]
    id = ["#" + x for x in element.attrs.get("id", [])]
    # order of precedence
    references = ["*", element.name] + classes + id
    debug_print(references)
    for ref in references:
        if ref in styles:
            for prop, value in styles[ref].items():
                debug_print(ref, prop, value)
                elem_style[prop] = value
    parent = element.parent
    while parent:
        if parent.name in styles:
            for prop, value in styles[parent.name].items():
                if prop not in elem_style:
                    elem_style[prop] = value
        parent = parent.parent
    return elem_style

def has_direct_contents(element):
    if not element.contents:
        return False

    for child in element.contents:
        if child.name is None:
            return True
    return False


def get_background_color(element):
    """returns the background color of an element and recurses to its parents if none exists.
    returns white if no parent has background color either."""
    style = element.get("style", {})
    bg = style.get("background-color", None)
    if bg is None:
        # Default to white if no color found
        bg = "#FFFFFF"
        # Check parent until a color is found or no more parents exist
        parent = element.parent
        while parent and bg == "#FFFFFF":
            parent_style = parent.get("style", {})
            parent_bg = parent_style.get("background-color", None)
            if parent_bg is not None:
                bg = parent_bg
            parent = parent.parent
    return css_to_hex(bg)

