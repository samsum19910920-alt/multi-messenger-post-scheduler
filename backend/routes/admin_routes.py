from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.app import db
from backend.models import User, Channel, ScheduledPost
from backend.utils.decorators import admin_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (Admin only)"""
    users = User.query.all()
    return {
        'users': [u.to_dict() for u in users]
    }, 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user (Admin only)"""
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    db.session.delete(user)
    db.session.commit()
    
    return {'message': 'User deleted successfully'}, 200

@admin_bp.route('/users/<int:user_id>/subscription', methods=['POST'])
@admin_required
def update_subscription(user_id):
    """Update user subscription (Admin only)"""
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    data = request.get_json()
    subscription_end = data.get('subscription_end')
    
    if subscription_end:
        try:
            user.subscription_end = datetime.fromisoformat(subscription_end)
            db.session.commit()
        except ValueError:
            return {'error': 'Invalid date format'}, 400
    
    return user.to_dict(), 200

@admin_bp.route('/statistics', methods=['GET'])
@admin_required
def get_statistics():
    """Get platform statistics (Admin only)"""
    return {
        'total_users': User.query.count(),
        'total_channels': Channel.query.count(),
        'total_posts': ScheduledPost.query.count(),
        'sent_posts': ScheduledPost.query.filter_by(is_sent=True).count()
    }, 200
