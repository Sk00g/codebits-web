import json
import utils
import model
import image_handler
from conf import default
from datetime import datetime
from flask import request, current_app, abort
from bson.objectid import ObjectId
from application import app

""" Handles a GET operation for a standard 'db_collection' MongoDB collection, for either a single value
    or the entire collection. May abort with 400 errors or return data 
"""
def _handle_get(db_collection, db, object_id, collection_singular=None):
    singular = collection_singular if collection_singular else '%s%s' % (db_collection[0].upper(), db_collection[1:-1])

    if object_id and not ObjectId.is_valid(object_id):
        utils.abort_400_error(utils.AppError.IDIsInvalid, str(object_id))

    if not object_id:
        return json.dumps([utils.prepare_mongo_dict(obj) for obj in db[db_collection].find()], indent=4)
    else:
        match = db[db_collection].find(dict(_id=ObjectId(object_id)))
        try:
            return json.dumps(utils.prepare_mongo_dict(match.next()))
        except StopIteration:
            utils.abort_400_error(utils.AppError.IDDoesNotExist, singular, str(object_id))

""" Handles a POST operation for a standard 'db_collection' MongoDB collection. Data is validated, and if
    successful an insert_one() operation is executed against the DB, and returns the resulting 'createdId' 
"""
def _handle_post(db_collection, data, db):
    error = model.validate_data(db_collection, data, db)
    if error:
        utils.abort_400_error(utils.AppError.InvalidData, error)

    response = db[db_collection].insert_one(data)

    return json.dumps(dict(createdId=str(response.inserted_id)))

""" Handles a PUT operation for a standard 'db_collection' MongoDB collection. Data is validated, and if
    successful an update_one() operation is executed against the DB, and returns the given 'updatedId'  
"""
def _handle_put(db_collection, data, db, object_id, collection_singular=None):
    singular = collection_singular if collection_singular else '%s%s' % (db_collection[0].upper(), db_collection[1:-1])

    if object_id and not ObjectId.is_valid(object_id):
        utils.abort_400_error(utils.AppError.IDIsInvalid, str(object_id))

    response = db[db_collection].update_one(dict(_id=ObjectId(object_id)),{ '$set': data })

    if response.matched_count != 1:
        utils.abort_400_error(utils.AppError.IDDoesNotExist, singular, str(object_id))

    return json.dumps(dict(updatedId=object_id))

""" Handles a DELETE operation for a standard 'db_collection' MongoDB collection. A delete_one() operation 
    is executed against the DB using the object_id string, and returns the given 'deletedId'  
"""
def _handle_delete(db_collection, db, object_id, collection_singular=None):
    singular = collection_singular if collection_singular else '%s%s' % (db_collection[0].upper(), db_collection[1:-1])

    if object_id and not ObjectId.is_valid(object_id):
        utils.abort_400_error(utils.AppError.IDIsInvalid, str(object_id))

    response = db[db_collection].delete_one(dict(_id=ObjectId(object_id)))

    if response.deleted_count != 1:
        utils.abort_400_error(utils.AppError.IDDoesNotExist, singular, str(object_id))

    return json.dumps(dict(deletedId=object_id))


""" 
    ----------------------------------------------------
    --------------- ROUTE DEFINITIONS ------------------
    ----------------------------------------------------
"""
@app.route('/api/categories', methods=['GET', 'POST'])
@app.route('/api/categories/<cat_id>', methods=['GET', 'PUT', 'DELETE'])
def categories(cat_id=None):
    if current_app.db_error:
        #TODO: Attempt periodic re-connect instead of just accepting the error
        abort(500, current_app.db_error['message'], current_app.db_error['code'])

    if request.method == 'GET':
        return _handle_get('categories', current_app.db, cat_id, 'Category')

    if request.method == 'POST':
        return _handle_post('categories', dict(**request.form), current_app.db)

    elif request.method == 'PUT':
        return _handle_put('categories', dict(**request.form), current_app.db, cat_id, 'Category')

    elif request.method == 'DELETE':
        return _handle_delete('categories', current_app.db, cat_id)

@app.route('/api/tags', methods=['GET', 'POST'])
@app.route('/api/tags/<tag_id>', methods=['GET', 'PUT', 'DELETE'])
def tags(tag_id=None):
    if current_app.db_error:
        #TODO: Attempt periodic re-connect instead of just accepting the error
        abort(500, current_app.db_error['message'], current_app.db_error['code'])

    if request.method == 'GET':
        return _handle_get('tags', current_app.db, tag_id)

    if request.method == 'POST':
        return _handle_post('tags', dict(**request.form), current_app.db)

    elif request.method == 'PUT':
        return _handle_put('tags', dict(**request.form), current_app.db, tag_id)

    elif request.method == 'DELETE':
        return _handle_delete('tags', current_app.db, tag_id)

@app.route('/api/codebits', methods=['GET', 'POST'])
@app.route('/api/codebits/<codebit_id>', methods=['GET', 'PUT', 'DELETE'])
def codebits(codebit_id=None):
    if current_app.db_error:
        #TODO: Attempt periodic re-connect instead of just accepting the error
        abort(500, current_app.db_error['message'], current_app.db_error['code'])

    if request.method == 'GET':
        response = json.loads(_handle_get('codebits', current_app.db, codebit_id))

        if type(response) == 'dict':
            response['imagePaths'] = image_handler.get_image_paths(response['_id'])
            return json.dumps(response, indent=4)

        for i in range(len(response)):
            response[i]['imagePaths'] = image_handler.get_image_paths(response[i]['_id'])
        return json.dumps(response, indent=4)

    if request.method == 'POST':
        response = json.loads(_handle_post('codebits',
                                           model.parse_form_data(request.form, 'codebits'),
                                           current_app.db))
        if response['createdId'] and request.files:
            image_handler.store_images(response['createdId'], request.files)

        return json.dumps(response)

    elif request.method == 'PUT':
        response = json.loads(_handle_put('codebits',
                                          model.parse_form_data(request.form, 'codebits'),
                                          current_app.db,
                                          codebit_id))
        if response['updatedId']:
            image_handler.delete_images(response['updatedId'])
            if request.files:
                image_handler.store_images(response['updatedId'], request.files)

        return json.dumps(response)

    elif request.method == 'DELETE':
        response = json.loads(_handle_delete('codebits', current_app.db, codebit_id))
        if response['deletedId']:
            image_handler.delete_images(response['deletedId'])

        return json.dumps(response)