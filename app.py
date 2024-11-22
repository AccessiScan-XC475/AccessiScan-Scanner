"""
This module sets up a Flask web server for a web accessibility scanner API.
It includes endpoints to assess text color contrast and large text accessibility
in provided HTML and CSS content. The API serves as a backend for scanning web content
to ensure accessibility standards are met.
"""

import os
from concurrent.futures import ThreadPoolExecutor
from base64 import b64encode
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from scanners.color_contrast_scanner import score_text_contrast
from scanners.text_scanner import score_text_accessibility
from scanners.alt_text import score_image_accessibility
from scanners.line_spacing import score_line_spacing  # Import the new module
from utils.append_score import append_score  # Import the new module
from utils.append_selection import log_selection

# Load environment variables
load_dotenv()

app = Flask(__name__)
cors = CORS(
    app, resources={r"/*": {"origins": "*"}}
)  # CHANGE THIS AFTER DOMAINS HAVE BEEN ASSIGNED

# GitHub OAuth constants
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
CHROME_EXTENSION_ID = os.getenv("CHROME_EXTENSION_ID")
REDIRECT_URI = f"https://{CHROME_EXTENSION_ID}.chromiumapp.org/"

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

@app.route("/api/auth/github/callback/extension", methods=["POST"])
def github_callback():
    """
    Endpoint to handle GitHub OAuth callback for the Chrome extension.
    Receives the authorization code and exchanges it for an access token.
    """
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "Authorization code is missing"}), 400

    # Exchange the authorization code for an access token
    token_url = "https://github.com/login/oauth/access_token"
    headers = {'Accept': 'application/json'}
    payload = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, json=payload, headers=headers, timeout=10)
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve access token"}), 500

    access_token = response.json().get("access_token")
    if not access_token:
        return jsonify({"error": "Access token not found in response"}), 500

    # Return the access token to the Chrome extension
    return jsonify({"access_token": access_token})

@app.route("/api/auth/github/revoke", methods=["POST"])
def revoke_github_token():
    """
    Revoke the GitHub OAuth token using the GitHub API.
    """
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    revoke_url = f"https://api.github.com/applications/{GITHUB_CLIENT_ID}/token"
    auth_header = f"{GITHUB_CLIENT_ID}:{GITHUB_CLIENT_SECRET}"
    headers = {
        "Authorization": f"Basic {b64encode(auth_header.encode()).decode()}",
        "Content-Type": "application/json",
    }
    payload = {"access_token": token}

    response = requests.delete(revoke_url, json=payload, headers=headers, timeout=10)
    if response.status_code == 204:  # Successful revocation
        return jsonify({"message": "Token revoked successfully"}), 200
    return jsonify({"error": response.json()}), response.status_code



@app.route("/api/scan-contrasting-colors", methods=["POST"])
def scan_color_contrast():
    """
    Endpoint to scan DOM and CSS for the text color contrast accessibility.
    Returns the color contrast score and list of inaccessible elements.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    [score, inaccessible_elements] = score_text_contrast(dom, css)
    print("score", score)
    print("Inaccessible elements:", inaccessible_elements)

    # potentially slow function to be run asynchronously
    with ThreadPoolExecutor() as executor:
        executor.submit(append_score, data.get("secret", ""), score)
        executor.submit(log_selection, "color-contrast")

    # Convert the inaccessible elements into string representations (e.g., HTML)
    inaccessible_html = [str(element) for element in inaccessible_elements]

    # Return the score and the inaccessible elements
    return {
        "score": f"{score}",
        "inaccessible_elements": inaccessible_html
    }


@app.route("/api/scan-large-text", methods=["POST"])
def scan_large_text():
    """
    Endpoint to scan large text in DOM and CSS for accessibility.
    Returns the accessibility score for large text and list of inaccesible elements.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    [score, inaccessible_elements] = score_text_accessibility(dom, css)
    print("score", score)
    print("Inaccessible elements:", inaccessible_elements)

    # potentially slow function to be run asynchronously
    with ThreadPoolExecutor() as executor:
        executor.submit(append_score, data.get("secret", ""), score)
        executor.submit(log_selection, "large-text")

    # Convert the inaccessible elements into string representations (e.g., HTML)
    text_inaccessible_html = [str(element) for element in inaccessible_elements]

    # Return the score and the inaccessible elements
    return {
        "score": score,
        "inaccessible_elements": text_inaccessible_html
    }


@app.route("/api/scan-images", methods=["POST"])
def scan_images():
    """
    Endpoint to scan DOM and CSS for image accessibility.
    Returns the number of images with alt text, total number of images,
    and the formatted score.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    # Get image accessibility score and element lists
    result = score_image_accessibility(dom, css)

    # Debugging: Print out the structure of image_accessibility_score
    print("Image accessibility score:", result)

    # Initialize default values for total images and images with alt text
    total_images = 0
    images_with_alt = 0
    score = 0

    # Check if the result is a dictionary and contains the necessary keys
    if isinstance(result, dict):
        total_images = result.get('total_images', 0)
        images_with_alt = result.get('images_with_alt', 0)
        if total_images == 0:
            score = 100
        else:
            score = (images_with_alt/total_images)*100
        # potentially slow function to be run asynchronously
        with ThreadPoolExecutor() as executor:
            executor.submit(append_score, data.get("secret", ""), score)
            executor.submit(log_selection, "alt-text")

    # Print debug information
    print(f"Total images: {total_images}, Images with alt text: {images_with_alt}")

    # Return the formatted score and image counts, ensuring they are set to 0 if no images are found
    return {
        "details": (
            f"There are {images_with_alt} image(s) with Alt Text"
            f" out of {total_images} total image(s)."
        ),
        "images_with_alt": images_with_alt,
        "total_images": total_images,
        "score": score
    }

@app.route("/api/scan-line-spacing", methods=["POST"])
def scan_line_spacing():
    """
    Endpoint to scan DOM and CSS for line spacing accessibility.
    Returns a score based on the percentage of text elements with sufficient line spacing.
    """
    data = request.get_json()
    dom = data.get("dom", "")
    css = data.get("css", "")

    [score, inaccessible_elements] = score_line_spacing(dom, css)
    print("score", score)
    print("Inaccessible elements:", inaccessible_elements)

    # potentially slow function to be run asynchronously
    with ThreadPoolExecutor() as executor:
        executor.submit(append_score, data.get("secret", ""), score)
        executor.submit(log_selection, "line-spacing")

    # Convert the inaccessible elements into string representations (e.g., HTML)
    inaccessible_html = [str(element) for element in inaccessible_elements]

    # Return the score and the inaccessible elements
    return {
        "score": f"{score}",
        "inaccessible_elements": inaccessible_html
    }

if __name__ == "__main__":
    if os.getenv("ENVIRONMENT") == "prod":
        app.run(debug=True, host="0.0.0.0", port=4200)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=4200)
