
from bs4 import BeautifulSoup

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