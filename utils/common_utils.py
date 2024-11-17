"""
Utility functions for text computations related to accessibility standards.
This module provides functions to compute text properties such as font size,
line height, and other text-related accessibility metrics.
"""
from services.css_parser import parse_css
from services.html_parser import parse_html, has_direct_contents


def parse_and_iterate_elements(html, css, tags_to_skip, element_handler):
    """
    Parses HTML and CSS content, iterates over elements, and calls the handler function for each element.
    """
    num_elements = 0
    num_accessible = 0
    inaccessible_elements = []

    soup = parse_html(html)
    styles = parse_css(css)

    for element in soup.find_all(True):
        if element.hidden or element.name in tags_to_skip or not has_direct_contents(element):
            continue  # Skip elements that are hidden or in the skip list

        num_elements += 1
        is_accessible = element_handler(element, styles)
        if is_accessible:
            num_accessible += 1
        else:
            inaccessible_elements.append(element)

    return num_elements, num_accessible, inaccessible_elements
