from bs4 import BeautifulSoup
import re
import cssutils

# Accessibility constants
NORMAL_TEXT_SIZE_PX = 16
LARGE_TEXT_SIZE_PX = 18
BOLD_LARGE_TEXT_SIZE_PX = 14
MIN_FONT_WEIGHT_BOLD = 700

DEBUG = False
TAGS_TO_SKIP = ["html", "title", "head", "style", "script"]

def debug_print(*args, **kwargs):
    """Prints messages only if debug mode is enabled."""
    if DEBUG:
        print(*args, **kwargs)

def score_text_accessibility(html_content, css_content):
    """Scores the text accessibility based on font size and weight."""
    num_elements = 0
    num_accessible = 0

    # Parse HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Parse CSS content
    css_parser = cssutils.CSSParser()
    parsed_stylesheet = css_parser.parseString(css_content)

    styles = {}
    for rule in parsed_stylesheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles[selector] = {}
            for prop in rule.style:
                styles[selector][prop.name] = prop.value

    for element in soup.find_all(True):
        if element.name in TAGS_TO_SKIP:
            continue

        num_elements += 1
        elem_style = get_computed_style(element, styles)

        # Get font size and weight from CSS
        font_size = elem_style.get("font-size", "16px")
        font_weight = int(elem_style.get("font-weight", "400"))

        # Check if the text is accessible based on size/weight
        if is_text_accessible(font_size, font_weight):
            num_accessible += 1

        debug_print(
            f"Element: {element.name}, Font Size: {font_size}, Font Weight: {font_weight}"
        )

    # Calculate accessibility score
    if num_elements == 0:
        return 100

    score = (num_accessible / num_elements) * 100
    trunc_score = round(score, 1)
    return trunc_score


def is_text_accessible(font_size: str, font_weight: int) -> bool:
    """Checks if the text size and weight comply with WCAG accessibility guidelines."""
    # Extract the numeric value from font size (assumes px units)
    font_size_value = int(re.match(r"\d+", font_size).group())

    # Check if it's large text
    if font_size_value >= LARGE_TEXT_SIZE_PX:
        return True
    if font_weight >= MIN_FONT_WEIGHT_BOLD and font_size_value >= BOLD_LARGE_TEXT_SIZE_PX:
        return True

    # If text is normal size, it should be at least 16px
    return font_size_value >= NORMAL_TEXT_SIZE_PX


def get_computed_style(element, styles):
    """Retrieves the computed styles (CSS) for an element."""
    elem_style = {}
    classes = ["." + x for x in element.attrs.get("class", [])]
    id = ["#" + x for x in element.attrs.get("id", [])]
    references = ["*", element.name] + classes + id
    for ref in references:
        if ref in styles:
            for prop, value in styles[ref].items():
                elem_style[prop] = value

    # Set default font size if not found in CSS
    if "font-size" not in elem_style:
        elem_style["font-size"] = "16px"  # Default size

    # Set default font weight if not found in CSS
    if "font-weight" not in elem_style:
        elem_style["font-weight"] = "400"  # Normal weight

    return elem_style


if __name__ == "__main__":
    """Example usage of text accessibility scanner."""
    html_content = """
    <html>
    <head><style>p { font-size: 20px; }</style></head>
    <body>
        <p class="normal">This is a paragraph.</p>
        <h1>This is a heading</h1>
        <p style="font-size: 12px;">Small text here.</p>
    </body>
    </html>
    """
    css_content = """
    p {
        font-size: 16px;
        font-weight: 400;
    }
    h1 {
        font-size: 32px;
        font-weight: 700;
    }
    """

    score = score_text_accessibility(html_content, css_content)
    print(f"Text Accessibility Score: {score}%")

if __name__ == "__main__":
    """Example usage of text accessibility scanner."""
    html_content = """
    <html>
    <head>
        <style>
            body {
                background-color: #FFFFFF; /* White background */
            }
            p {
                font-size: 8px; /* Very small font size */
                color: #CCCCCC; /* Light gray text color */
            }
            h1 {
                font-size: 10px; /* Very small heading size */
                color: #CCCCCC; /* Light gray text color */
            }
        </style>
    </head>
    <body>
        <p class="normal">This is a barely readable paragraph.</p>
        <h1>This is an almost invisible heading</h1>
        <p style="font-size: 6px; color: #D3D3D3;">Extremely small and light text here.</p>
    </body>
    </html>
    """
    css_content = """
    p {
        font-size: 10px; /* Small font size */
        font-weight: 400;
    }
    h1 {
        font-size: 12px; /* Small heading */
        font-weight: 700;
    }
    """

    score = score_text_accessibility(html_content, css_content)
    print(f"Text Accessibility Score: {score}%")
