#!/bin/bash 
source bin/activate && 
(pip install -r requirements.txt || pip3 install -r requirements.txt) &&
(python app.py || python3 app.py) && 
deactivate
