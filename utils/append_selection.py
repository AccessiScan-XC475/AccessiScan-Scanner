""" 
updates a users score history
"""
from requests import post
import os

def log_selection(name:str):
    # save calls to backend and db
    if name == "":
        return

    # determine backend domain based on environment
    domain = "https://accessiscan.vercel.app" \
        if os.getenv("ENVIRONMENT") != "dev" else \
        "http://localhost:3000"

    # get secret to keep between backend and scanner
    a_sec = os.getenv("ACCESSISCAN_SECRET")
    endpoint =f"{domain}/api/accessibility-selection?&name={name}&accessiscanSecret={a_sec}" 
    print("endpoint: ", endpoint)
    try:
        post(endpoint)
    except:
        print("error appending score")
