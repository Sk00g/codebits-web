import utils
from cerberus import Validator

_validators = {
    'categories': Validator({
        'name': { 'type': 'string', 'minlength': 3, 'maxlength': 32 }
    },
    require_all=True),
    'tags': Validator({
        'name': { 'type': 'string', 'minlength': 2, 'maxlength': 32 },
        'description': { 'type': 'string', 'maxlength': 512 }
    },
    require_all=True),
    'codebits': Validator({
        # Metadata
        'dateCreated': { 'type': 'datetime' },
        'lastUpdated': { 'type': 'datetime' },
        'createdFrom': { 'type': 'string' },
        # Core Content
        'title': { 'type': 'string', 'maxlength': 32 },
        'text': { 'type': 'string', 'minlength': 3, 'maxlength': 256 * 1024 },
        """ links, codeSnippets, and images come in the format: {
                'url | text | path': [LINK URL | CODE TEXT | IMAGE PATH],
                'startChar': [INT]
            }
        """
        'links': { 'type': 'list' },
        'codeSnippets': { 'type': 'list' },
        'images': { 'type': 'list' },
        # Association
        'category': { 'check_with': utils.is_valid_objectid },
        'tags': { 'type': 'list' },
    })
}

_collection_settings = {
    'categories': {
        'uniqueFields': ['name']
    },
    'tags': {
        'uniqueFields': ['name']
    },
    'codebits': {
        'uniqueFields': ['title']
    }
}

def validate_data(object_type, data, db=None):
    if object_type not in _validators:
        return "No validation data exists for object_type '%s'" % object_type

    if db and object_type in _collection_settings:
        settings = _collection_settings[object_type]
        if 'uniqueFields' in settings:
            for field in settings['uniqueFields']:
                match = db[object_type].find_one({ field: data[field] })
                if match:
                    return "One '%s' object with '%s' value of '%s' already exists" % (object_type, field, data[field])

    if _validators[object_type].validate(data):
        return None
    else:
        return utils.capitalize_error_lists(_validators[object_type].errors)[0]