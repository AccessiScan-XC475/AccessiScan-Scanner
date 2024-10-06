from flask import Flask, redirect, request, url_for
from flask_cors import CORS
from scanner import score_text_contrast

app = Flask(__name__)
cors = CORS(
    app, resources={r"/*": {"origins": "*"}}
)  # CHANGE THIS AFTER DOMAINS HAVE BEEN ASSIGNED


@app.route("/")
def home():
    # # CHANGE AFTER DOMAINS HAVE BEEN ASSIGNED
    # return redirect(url_for("http://localhost:3000"))
    return "please visit: http://localhost:3000"


@app.route("/api/health", methods=["GET"])
def health():
    return "OK"


@app.route("/api/scan", methods=["POST"])
def scan():
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)
