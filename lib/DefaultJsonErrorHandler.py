from flask import jsonify
from json import dumps
from json import loads
from traceback import format_exception_only
from werkzeug.exceptions import HTTPException
from flask_principal import Permission

def make_json_error(ex):
    """Turn an exception into a chunk of JSON"""
    response = jsonify({})    
    response_dict = loads(response.get_data(as_text=True))
    if hasattr(ex, 'state_go'):
        response_dict['state_go'] = ex.state_go
    if isinstance(ex, HTTPException):
        response.status_code = ex.code
        if isinstance(ex.description, Permission):
            response_dict['message'] = "Permission denied"
        else:
            response_dict['message'] = str(ex.description)
    else:
        response.status_code = 500
        response_dict['message'] = str(ex)
    if response.status_code == 500:
        response_dict['stack'] = str(format_exception_only(type(ex), ex))
    response.set_data(dumps(response_dict))
    return response

