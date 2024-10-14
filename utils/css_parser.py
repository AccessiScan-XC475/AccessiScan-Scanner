"""
This module provides a utility function for parsing CSS content into a dictionary of styles.
"""
import cssutils

def parse_css(css_content):
    """
    Parses CSS content and returns a dictionary where the keys are CSS selectors
    and the values are dictionaries of style properties and their corresponding values.

    Args:
        css_content (str): The raw CSS content as a string.

    Returns:
        A dictionary where each key is a CSS selector and the corresponding value
              is another dictionary of style properties (e.g., 'font-size') 
              and their values (e.g., '16px').
    """
    css_parser = cssutils.CSSParser()
    parsed_stylesheet = css_parser.parseString(css_content)
    styles = {}

    # Iterate through all the rules in the stylesheet
    for rule in parsed_stylesheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles[selector] = {}
            # Add each property and its value to the styles dictionary
            for prop in rule.style:
                styles[selector][prop.name] = prop.value
    return styles
