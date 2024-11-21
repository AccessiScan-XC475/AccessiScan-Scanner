""" 
updates a users score history
"""
from utils.backend_request import post_backend

def append_score(secret:str, score):
    """ add score to user's score history """
    # save calls to backend and db
    if secret == "":
        return

    endpoint =f"/api/append?score={int(score)}&secret={secret}"
    try:
        post_backend(endpoint)
    except:
        print("error appending score")
