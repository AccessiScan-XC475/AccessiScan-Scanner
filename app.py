"""
This module sets up a Flask web server for a web accessibility scanner API.
It includes endpoints to assess text color contrast and large text accessibility
in provided HTML and CSS content. The API serves as a backend for scanning web content
to ensure accessibility standards are met.
"""
from flask import Flask, request
from flask_cors import CORS
from scanners.color_contrast_scanner import score_text_contrast
from scanners.text_scanner import score_text_accessibility

app = Flask(__name__)
cors = CORS(
    app, resources={r"/*": {"origins": "*"}}
)# CHANGE THIS AFTER DOMAINS HAVE BEEN ASSIGNED


@app.route("/")
def home():
    """
    Home route serving as placeholder URL. This should be updated
    after domains have been assigned.
    """

    # return redirect(url_for("http://localhost:3000"))
    return "please visit: http://localhost:3000"


@app.route("/api/health", methods=["GET"])
def health():
    """
    Health check endpoint to ensure api is working.
    Returns OK if the API is running.
    """
    return "OK"


@app.route("/api/scan-contrasting-colors", methods=["POST"])
def scan():
    """
    Endpoint to scan DOM and CSS for the text color contrast accessibility.
    Returns the color contrast score.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    [score, accessible_elements, inaccessible_elements] = score_text_contrast(dom, css)
    print("score", score)
    print("Inaccessible elements:", inaccessible_elements)
    print("Accessible elements:", accessible_elements)

    # Convert the inaccessible elements into string representations (e.g., HTML)
    inaccessible_html = [str(element) for element in inaccessible_elements]

    # Return the score and the inaccessible elements
    return {"score": score, "inaccessible_elements": inaccessible_html}


@app.route("/api/scan-large-text", methods=["POST"])
def scan_large_text():
    """
    Endpoint to scan large text in DOM and CSS for accessibility.
    Returns the accessibility score for large text.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    [score, accessible_elements, inaccessible_elements] = score_text_accessibility(dom, css)
    print("score", score)
    print("Inaccessible elements:", inaccessible_elements)
    print("Accessible elements:", accessible_elements)

    # Convert the inaccessible elements into string representations (e.g., HTML)
    text_inaccessible_html = [str(element) for element in inaccessible_elements]

    # Return the score and the inaccessible elements
    return {"score": score, "inaccessible_elements": text_inaccessible_html}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)
  