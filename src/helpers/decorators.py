from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity 
from flask_jwt_extended import verify_jwt_in_request

from src.constants.http_status_codes import HTTP_401_UNAUTHORIZED

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_identity()
            if claims['flag'] == True:
                return fn(*args, **kwargs)
            else:
                return jsonify({
                    'message': False,
                    'error': 'Only admin can access this resource'
                }), HTTP_401_UNAUTHORIZED
        return decorator
    return wrapper

