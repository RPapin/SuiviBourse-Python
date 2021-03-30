from flask import Flask, request
import json
from os import path, listdir
import os.path
from os.path import isfile, join
import getOldData as god
app = Flask(__name__)
# app.config["DEBUG"] = True

onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
pathData = os.path.join(os.getcwd(), 'data.json')
@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
# A route to return all data.
@app.route('/data', methods=['GET'])
def api_all():
    
    with open(pathData) as json_file:
        return json.load(json_file)
@app.route('/fecthLastData', methods=['GET'])
def fetchLastData():
    god.main()
    with open(pathData) as json_file:
        return json.load(json_file)
        
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
if __name__ == "__main__":
    app.run(host='0.0.0.0')