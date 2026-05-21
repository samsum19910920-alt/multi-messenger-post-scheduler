from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash
import os

"""
Decorators برای احراز هویت و تایید Admin
"""

def admin_required(f):
    """
    Decorator برای بررسی Admin Key
    تمام endpoint‌های حساس نیاز به این decorator دارند
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_key = request.headers.get('X-Admin-Key')
        valid_key = os.getenv('ADMIN_PASSWORD_HASH', 'admin123')
        
        if not admin_key or admin_key != valid_key:
            return jsonify({'error': 'Unauthorized - Invalid Admin Key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


def require_json(f):
    """
    Decorator برای بررسی Content-Type JSON
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function
