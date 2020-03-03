import os
import json
import pymongo
import pymongo.errors
import utils
from flask import Flask, render_template, request, redirect, url_for, abort, current_app


app = Flask(__name__)

# Store the database connection pool (MongoClient) on the app for access via the 'current_app' global on each request
try:
    client = pymongo.MongoClient("mongodb+srv://admin:nh6016asc@codebits-cluster-8qcxg.gcp.mongodb.net/codebits?retryWrites=true&w=majority")
    app.db = client.codebits
    app.db_error = None
except pymongo.errors.ConfigurationError as err:
    #TODO: Log this error somewhere appropriate
    app.db_error = utils.AppError.DatabaseConnectionError

app.config.from_object('conf.default')

@app.errorhandler(404)
def error_invalid_url(error):
    return json.dumps(dict(code=0, message='Invalid URL')), 404

@app.errorhandler(405)
def error_method_not_allowed(error):
    return json.dumps(dict(code=0, message='Method Not Allowed')), 405

@app.errorhandler(400)
def error_invalid_data(error):
    return json.dumps(dict(code=error.response, message=error.description)), 400

@app.errorhandler(500)
def error_server_error(error):
    return json.dumps(dict(code=error.response, message=error.description)), 500

""" Importing API Route Files """
import api

@app.route('/', methods=['GET', 'POST'])
def get_index():
    # return dict(name='Scott', age=27)

    # abort(404)
#     print(request.args)

    # return redirect(url_for('category'))

    if request.method == 'POST' and request.files:
        print(request.files)
        f = request.files['imageFile']
        f.save('./static/images/%s' % f.filename)

    return render_template('index.html')
    # return "<h1>HELLO Azure. Took you long enough...</h1>"

@app.route('/api/files', methods=['GET'])
def files():
    return str(os.listdir('./static/images'))
