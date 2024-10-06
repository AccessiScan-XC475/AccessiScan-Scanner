from bs4 import BeautifulSoup
import re
import cssutils
import itertools
import math
from PIL import ImageColor

NORMAL_TEXT_CONTRAST_RAIO = 4.5
OTHER_CONTRACT_RATIO = 3


def score_text_contrast(html_content, css_content):
    """parses html and css content.
    returns a score based on percentage of text elements with
    adequate contrast between text and background colors"""
    num_elements = 0
    num_accessible = 0

    # create html parser from html content / dom
    soup = BeautifulSoup(html_content, "html.parser")

    # create css parser wih css content
    css_parser = cssutils.CSSParser()
    css_rules = css_parser.parseString(css_content)

    # compute styles for elements of dom
    computed_styles = get_computed_style(soup, css_rules)

    # for each element, compare background color to text color
    for element in soup.find_all():
        num_elements += 1
        style = computed_styles.get(element)
        if style:
            color = style["color"]
            background_color = style["background-color"]

            # convert from hex to rgb tuple for easier computation
            color_rgb = hex_to_rgb(color) if color.startswith("#") else (0, 0, 0)
            background_rgb = (
                hex_to_rgb(background_color)
                if background_color.startswith("#")
                else (255, 255, 255)
            )  # default background color to white

            ratio = contrast_ratio(color_rgb, background_rgb)
            if ratio >= NORMAL_TEXT_CONTRAST_RAIO:
                num_accessible += 1
            print(
                f"Element: {element.name}, Text Color: {color}, Background Color: {background_color}, Contrast Ratio: {ratio:.2f}"
            )
        else:
            # assume colors are accessible if not styling available (white background with black text)
            num_accessible += 1

    # cannot divide by zero
    # if no element, no example of not enough contrast
    if num_elements == 0:
        return 100

    score = (num_accessible / num_elements) * 100  # to percentage
    trunc_score = math.floor(score * 10) / 10  # truncate to tenths
    print(num_accessible, num_elements, trunc_score)
    return trunc_score


# compute color and background color styling
def get_computed_style(soup, css_rules):
    """returns dict of elements and their text and background colors"""
    styles = {}
    for rule in css_rules:
        if rule.type == rule.STYLE_RULE:
            selectors = rule.selectorText.split(",")
            for selector in selectors:
                print(selector)
                try:
                    for el in soup.select(selector.strip()):
                        color = css_to_hex(rule.style.getPropertyValue("color"))
                        if color is None:
                            # default color is black
                            color = "#000000"
                        print("color", color)
                        bg = get_background_color(el)
                        print("bg", bg)
                        print(color, bg)
                        styles[el] = {
                            "color": color,
                            "background-color": bg,
                        }
                except:
                    print("skipping.,.")
                    continue
    return styles


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


def css_to_hex(color):
    """converts css color into hex"""
    # check if valid hex
    if bool(re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color)):
        return color

    # check if is valid string rgb tuple
    rgb_match = re.match(
        r"^\s*rgb\s*\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)\s*$",
        color,
        re.IGNORECASE,
    )
    if rgb_match:
        # get rgb values
        r, g, b = map(int, rgb_match.groups())

        # check all rgb values are valid
        if all(0 <= x <= 255 for x in (r, g, b)):
            return rgb_to_hex((r, g, b))

    # try to convert css color word (eg red) to hex
    try:
        # css color to rgb tuple
        rgb = ImageColor.getrgb(color)
        # tuple to hex
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    except:
        return None


def rgb_to_hex(rgb):
    """converts an rgb tuple or list to its hex string.
    assumes valid rgb input"""
    r, g, b = [x for x in rgb]
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex_color):
    """converts a hexcode color into an rgb tuple.
    assumes valid hex input"""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        return tuple(int(hex_color[i] + hex_color[1], 16) for i in range(3))
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def calculate_luminance(rgb: tuple[int, ...]):
    """calculates the apparent lumunicance of the input color.
    assumes color is rgb tuple with min 0 and max 255"""

    def conv(color):
        i = float(color) / 255
        if i < 0.03928:
            return i / 12.92
        return ((i + 0.055) / 1.055) ** 2.4

    # https://www.w3.org/TR/WCAG20/#relativeluminancedef
    r, g, b = [conv(x) for x in rgb]

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


# calculate the contrast ratio
def contrast_ratio(rgb1: tuple[int, ...], rgb2: tuple[int, ...]):
    """returns the contrast ratio between two colors truncated to the hundreths place"""
    l_1 = calculate_luminance(rgb1)
    l_2 = calculate_luminance(rgb2)

    lighter = max(l_1, l_2)
    darker = min(l_1, l_2)

    print(lighter, darker)

    # https://www.accessibility-developer-guide.com/knowledge/colours-and-contrast/how-to-calculate/
    ratio = (lighter + 0.05) / (darker + 0.05)
    return math.floor(ratio * 100) / 100.0


if __name__ == "__main__":
    """testing calculated contrast ratios"""

    def test(c1, c2, expected):
        print(f"\ncomparing {c1} and {c2}")

        h1 = hex_to_rgb(c1)
        h2 = hex_to_rgb(c2)

        x = contrast_ratio(h1, h2)

        success = x == expected
        print(x, expected, success)
        return success

    # test values calculated with https://webaim.org/resources/contrastchecker/
    test("#ffffff", "#000000", 21)
    test("#c9a2d8", "#915e03", 2.53)
    test("#5bbb4f", "#fa4003", 1.49)
    test("#284b2f", "#7ef9dd", 7.7)
    test("#6b69ea", "#07a09d", 1.34)
    test("#ddc6e2", "#52dbc6", 1.07)
    test("#77c551", "#d8a85d", 1.02)

    print("\n\nchecking our color palette")
    color_palette = [
        "#90D8B2",
        "#8DD2DD",
        "#8BABF1",
        "#8B95F6",
        "#9B8BF4",
    ]
    for c1, c2 in itertools.combinations(color_palette, 2):
        rgb1 = hex_to_rgb(c1)
        rgb2 = hex_to_rgb(c2)
        print(contrast_ratio(rgb1, rgb2))
