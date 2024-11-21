""" 
updates a users score history
"""
from requests import post
import os

def appendScore(secret:str, score):
    # save calls to backend and db
    if secret == "":
        return

    # determine backend domain based on environment
    domain = "https://accessiscan.vercel.app" \
        if os.getenv("ENVIRONMENT") != "dev" else \
        "http://localhost:3000"

    # get secret to keep between backend and scanner
    a_sec = os.getenv("ACCESSISCAN_SECRET")
    endpoint =f"{domain}/api/append?score={int(score)}&secret={secret}&accessiscanSecret={a_sec}" 
    print("endpoint: ", endpoint)
    try:
        post(endpoint)
    except:
        print("error appending score")
