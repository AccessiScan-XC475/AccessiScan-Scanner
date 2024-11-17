from services.css_parser import parse_css
from services.html_parser import parse_html, has_direct_contents


def parse_and_iterate_elements(html_content, css_content, tags_to_skip, element_handler):
    """
    Parses HTML and CSS content, iterates over elements, and calls the handler function for each element.
    :param html_content: HTML content to parse.
    :param css_content: CSS content to parse.
    :param tags_to_skip: List of tags to skip.
    :param element_handler: Function to handle each element during iteration.
    :return: Total elements processed and accessible elements.
    """
    num_elements = 0
    num_accessible = 0
    inaccessible_elements = []

    soup = parse_html(html_content)
    styles = parse_css(css_content)

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
