import flask
import json
from os import path
import os.path
import getOldData as god
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
# A route to return all data.
@app.route('/api/v1/data', methods=['GET'])
def api_all():
    pathData = os.path.join(os.getcwd(), 'Python/data.json')
    print(pathData)
    with open(pathData) as json_file:
        return json.load(json_file)
@app.route('/api/v1/fecthLastData', methods=['GET'])
def fetchLastData():
    god.main()
    pathData = os.path.join(os.getcwd(), 'Python/data.json')
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
app.run()