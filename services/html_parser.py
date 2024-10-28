"""
This module provelement_ides utilities for parsing and extracting information
from HTML content, including computing styles and retrieving background colors.
It also includes functions to check for direct content and parse HTML elements.
"""
from bs4 import BeautifulSoup
from utils.contrast_utils import css_to_hex
from utils.debug import debug_print

def parse_html(html_content):
    """
    Parses the provelement_ided HTML content and returns a BeautifulSoup object.
    
    Args:
        html_content (str): The raw HTML content to parse.
    
    Returns:
        BeautifulSoup: The parsed HTML content.
    """
    return BeautifulSoup(html_content, "html.parser")

def get_computed_style(element, styles):
    """
    Computes the final style of an HTML element based on its classes, id, and tag name.
    Args:
        element (Tag): The HTML element whose style is being computed.
        styles (dict): The parsed CSS styles dictionary.
    Returns:
        dict: The computed style dictionary for the element.
    """
    elem_style = {}

    # First check inline styles (highest priority)
    if 'style' in element.attrs:
        inline_styles = element.attrs['style'].split(';')
        for prop_value in inline_styles:
            if ':' in prop_value:
                prop, value = prop_value.split(':', 1)
                elem_style[prop.strip()] = value.strip()  # Inline styles should override all others

    # Apply external styles by priority (classes, ids, tags)
    classes = ["." + x for x in element.attrs.get("class", [])]
    element_id = ["#" + x for x in element.attrs.get("id", [])]
    references = ["*", element.name] + classes + element_id
    references.reverse()  # Prioritize IDs and classes over tags

    debug_print(references)
    for ref in references:
        if ref in styles:
            for prop, value in styles[ref].items():
                # Apply external styles only if they haven't been set by inline styles
                if prop not in elem_style:
                    elem_style[prop] = value

    # Handle parent inheritance AFTER inline and external styles
    parent = element.parent
    while parent:
        if parent.name in styles:
            for prop, value in styles[parent.name].items():
                if prop not in elem_style:  # Only apply if not already set
                    elem_style[prop] = value
        parent = parent.parent
    return elem_style

def has_direct_contents(element):
    """
    Checks if the given element has direct textual content, ignoring nested tags.

    Args:
        element (Tag): The HTML element to check.

    Returns:
        bool: True if the element has direct text content, False otherwise.
    """
    if not element.contents:
        return False

    for child in element.contents:
        if child.name is None:
            return True
    return False


def get_background_color(element):
    """
    Retrieves the background color of an HTML element, recursing through
    its parent elements if no background color is set.

    Args:
        element (Tag): The HTML element whose background color is needed.

    Returns:
        str: The background color in hexadecimal format (e.g., #FFFFFF).
    """
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
