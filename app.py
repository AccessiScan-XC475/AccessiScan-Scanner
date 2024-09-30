from flask import Flask, redirect, request, url_for 
from flask_cors import CORS
from random import randint 

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins":"*"}}) # CHANGE THIS AFTER DOMAINS HAVE BEEN ASSIGNED

@app.route("/")
def home():
    # # CHANGE AFTER DOMAINS HAVE BEEN ASSIGNED
    # return redirect(url_for("http://localhost:3000"))
    return "please visit: http://localhost:3000"

@app.route('/api/health', methods=["GET"])
def health():
    return "OK"

@app.route('/api/scan', methods=["POST"])
def scan():
    body = request.data
    print(body)
    return f"{randint(1, 100)}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)
