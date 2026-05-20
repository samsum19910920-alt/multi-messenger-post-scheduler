from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models import User

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return user.to_dict(), 200

@user_bp.route('/subscription-status', methods=['GET'])
@jwt_required()
def get_subscription_status():
    """Get user subscription status"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return {
        'is_active': user.is_subscription_active(),
        'subscription_end': user.subscription_end.isoformat() if user.subscription_end else None
    }, 200
