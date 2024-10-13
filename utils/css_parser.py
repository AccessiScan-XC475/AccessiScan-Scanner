import cssutils

def parse_css(css_content):
    # Parse CSS and return a dictionary of styles
    css_parser = cssutils.CSSParser()
    parsed_stylesheet = css_parser.parseString(css_content)
    styles = {}
    for rule in parsed_stylesheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles[selector] = {}
            for prop in rule.style:
                styles[selector][prop.name] = prop.value
    return styles