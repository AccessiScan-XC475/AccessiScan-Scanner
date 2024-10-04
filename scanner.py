from bs4 import BeautifulSoup
import cssutils
import numpy as np

NORMAL_TEXT_CONTRAST_RAIO = 4.5
OTHER_CONTRACT_RATIO = 3

def score_text_contrast(html_content, css_content):
    num_elements = 0 
    num_accessible = 0

    # create html parser from html content / dom
    soup = BeautifulSoup(html_content, 'html.parser')

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
            color = style['color']
            background_color = style['background-color']
            
            # convert from hex to rgb tuple for easier computation
            color_rgb = hex_to_rgb(color) if color.startswith('#') else (0, 0, 0)
            background_rgb = hex_to_rgb(background_color) if background_color.startswith('#') else (255, 255, 255)  # default background color to while

            ratio = contrast_ratio(color_rgb, background_rgb)
            if ratio > NORMAL_TEXT_CONTRAST_RAIO:
                num_accessible += 1
            print(f"Element: {element.name}, Text Color: {color}, Background Color: {background_color}, Contrast Ratio: {ratio:.2f}") 
        else:
            # assume colors are accessible if not styling available (white background with black text)
            num_accessible += 1
    return num_accessible / num_elements if num_elements != 0 else None

# compute color and background color styling
def get_computed_style(soup, css_rules):
    styles = {}
    for rule in css_rules:
        if rule.type == rule.STYLE_RULE:
            selectors = rule.selectorText.split(',')
            for selector in selectors:
                for el in soup.select(selector.strip()):
                    styles[el] = {
                        'color': rule.style.getPropertyValue('color'),
                        'background-color': rule.style.getPropertyValue('background-color'),
                    }
    return styles

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def calculate_luminance(rgb: tuple[int, ...]):
    # https://www.w3.org/TR/WCAG20/#relativeluminancedef
    r, g, b = [x / 255 for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

# calculate the contrast ratio
def contrast_ratio(rgb1:tuple[int, ...], rgb2:tuple[int, ...]):
    l_1 = calculate_luminance(rgb1)
    l_2 = calculate_luminance(rgb2) 

    lighter = max(l_1, l_2)
    darker = min(l_1, l_2)

    # https://www.accessibility-developer-guide.com/knowledge/colours-and-contrast/how-to-calculate/
    return (lighter + 0.05) / (darker + 0.05)


if __name__ == "__main__":
    c1 = "#c9a2d8"
    c2 = "#915e03"

    h1 = hex_to_rgb(c1)
    h2 = hex_to_rgb(c2)

    x = contrast_ratio(h1, h2)
    print(x)
