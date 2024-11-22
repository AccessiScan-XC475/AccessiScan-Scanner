""" 
updates a users score history
"""
import requests
from utils.backend_request import post_backend

def append_score(secret:str, score):
    """ add score to user's score history """
    # save calls to backend and db
    if secret == "":
        return

    endpoint =f"/api/append?score={int(score)}&secret={secret}"
    try:
        post_backend(endpoint)
    except requests.exceptions.ConnectionError:
        print("error appending score. ensure the backend is running")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred when appending score: {e}")
