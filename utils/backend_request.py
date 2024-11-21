"""
make requests to the backend. automatically determines the correct domain and includes secret
"""
import os
from requests import post

t = 1000

def post_backend(endpoint: str):
    """ function to make a post request to backend that contains accessiscan secret """

    # determine backend domain based on environment
    domain = "https://accessiscan.vercel.app" \
        if os.getenv("ENVIRONMENT") != "dev" else \
        "http://localhost:3000"


    a_sec = os.getenv("ACCESSISCAN_SECRET")
    if "?" in endpoint:
        return post(domain + endpoint + f"&accessiscanSecret={a_sec}", timeout=t)
    return post(domain + endpoint + f"?accessiscanSecret={a_sec}", timeout=t)
