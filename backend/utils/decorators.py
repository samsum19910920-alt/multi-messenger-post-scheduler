from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
import os
from werkzeug.security import check_password_hash

def admin_required(fn):
    """
    Decorator to check if user is admin
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        # In production, check user role from database
        # For now, check Authorization header
        auth_header = request.headers.get('X-Admin-Key')
        admin_key = os.getenv('ADMIN_PASSWORD_HASH')
        
        if not auth_header or not check_password_hash(admin_key, auth_header):
            return {'error': 'Unauthorized'}, 403
        
        return fn(*args, **kwargs)
    return wrapper
