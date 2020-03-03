from datetime import datetime
from bson.objectid import ObjectId
from conf import default
from flask import abort

class AppError:
    IDDoesNotExist = dict(code=0xA0, message='{1} of id {2} does not exist')
    IDIsInvalid = dict(code=0xA1, message='Object id {1} is invalid')
    InvalidData = dict(code=0xA2, message='{1}')
    DatabaseConnectionError = dict(code=0xA3, message='Database server could not be reached')

def abort_400_error(err, *args):
    message = err['message']
    for i in range(len(args)):
        message = message.replace('{%d}' % (i + 1), args[i])

    abort(400, message, err['code'])

def get_enum_list(class_name):
    return [enum for enum in dir(class_name) if not enum.startswith('__')]

def is_valid_objectid_accept_none(field, value, error):
    if value and not ObjectId.is_valid(value):
        error(field, 'not a valid ObjectId')

def is_valid_objectid(field, value, error):
    if not ObjectId.is_valid(value):
        error(field, 'not a valid ObjectId')

def enum_has_property(enum_class, prop):
    return prop in [mem for mem in dir(enum_class) if not mem.startswith('__')]

def prepare_mongo_list(array):
    for i in range(len(array)):
        if type(array[i]) == datetime:
            array[i] = array[i].strftime(default.DATETIME_FORMAT)
        elif type(array[i]) == dict:
            array[i] = prepare_mongo_dict(array[i])
        elif type(array[i]) == list:
            array[i] = prepare_mongo_list(array[i])

    return array

def prepare_mongo_dict(data):
    if '_id' in data and type(data['_id']) == ObjectId:
        data['_id'] = str(data['_id'])

    for field in data:
        if type(data[field]) == datetime:
            data[field] = data[field].strftime(default.DATETIME_FORMAT)
        elif type(data[field]) == dict:
            data[field] = prepare_mongo_dict(data[field])
        elif type(data[field]) == list:
            data[field] = prepare_mongo_list(data[field])

    return data

def capitalize_error_lists(errors):
    for field in errors:
        for i in range(len(errors[field])):
            errors[field][i] = "%s%s" % (errors[field][i][0].upper(), errors[field][i][1:])

    return ['%s: %s' % (field, errors[field][0]) for field in errors]
