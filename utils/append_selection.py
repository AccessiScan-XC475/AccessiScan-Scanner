""" 
updates a users score history
"""
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
    except:
        print("error appending score")
