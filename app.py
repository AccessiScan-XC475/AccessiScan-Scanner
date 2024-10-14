from flask import Flask, request
from flask_cors import CORS
from scanner import score_text_contrast
from textscanner import score_text_accessibility

app = Flask(__name__)
cors = CORS(
    app, resources={r"/*": {"origins": "*"}}
)  # CHANGE THIS AFTER DOMAINS HAVE BEEN ASSIGNED


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

    # Print HTML
    print("HTML Content:")
    print(dom)

    # Print 2 empty lines
    print("\n\n")

    # Print CSS
    print("CSS Content:")
    print(css)

    score = score_text_contrast(dom, css)
    print("score", score)

    return f"{score}"


@app.route("/api/scan-large-text", methods=["POST"])
def scan_large_text():
    """
    Endpoint to scan large text in DOM and CSS for accessibility.
    Returns the accessibility score for large text.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    # Print a simple message to confirm this endpoint works
    print("Large text scan endpoint hit")

    text_score = score_text_accessibility(dom, css)
    print ("score", text_score)
    return f"{text_score}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)
