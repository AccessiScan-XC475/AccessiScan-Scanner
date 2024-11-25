""" 
updates a users score history
"""
from urllib.parse import urlencode
import requests
from utils.backend_request import post_backend


def append_score(secret, score, href, selection):
    """ add score to user's score history """
    # save calls to backend and db
    if secret == "":
        print("no secret")
        return

    href = urlencode({"href": href})
    endpoint =f"/api/append?score={int(score)}&secret={secret}&{href}&selection={selection}"
    try:
        print("posting to backkedn")
        post_backend(endpoint)
    except requests.exceptions.ConnectionError:
        print("error appending score. ensure the backend is running")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred when appending score: {e}")
