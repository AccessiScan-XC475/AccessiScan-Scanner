""" 
updates a users score history
"""
import requests
from utils.backend_request import post_backend

def log_selection(name:str):
    """ log accessibility selection in backend """
    # save calls to backend and db
    if name == "":
        return
    # get secret to keep between backend and scanner
    endpoint =f"/api/accessibility-selection?&name={name}"
    print("endpoint: ", endpoint)
    try:
        post_backend(endpoint)
    except requests.exceptions.ConnectionError:
        print("error logging selection. ensure the backend is running")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred when logging selection: {e}")
