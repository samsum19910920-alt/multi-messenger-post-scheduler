from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models import User, Channel
from backend.utils.validators import validate_channel_data

channel_bp = Blueprint('channel', __name__, url_prefix='/api/channels')

@channel_bp.route('/', methods=['GET'])
@jwt_required()
def get_channels():
    """Get all channels for current user"""
    user_id = get_jwt_identity()
    channels = Channel.query.filter_by(user_id=user_id).all()
    
    return {
        'channels': [ch.to_dict() for ch in channels]
    }, 200

@channel_bp.route('/', methods=['POST'])
@jwt_required()
def add_channel():
    """Add new channel"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not validate_channel_data(data):
        return {'error': 'Invalid channel data'}, 400
    
    channel = Channel(
        user_id=user_id,
        messenger_type=data['messenger_type'],
        channel_id=data['channel_id'],
        channel_name=data.get('channel_name'),
        channel_username=data.get('channel_username'),
        bot_token=data['bot_token']
    )
    
    db.session.add(channel)
    db.session.commit()
    
    return channel.to_dict(), 201

@channel_bp.route('/<int:channel_id>', methods=['DELETE'])
@jwt_required()
def delete_channel(channel_id):
    """Delete channel"""
    user_id = get_jwt_identity()
    channel = Channel.query.filter_by(id=channel_id, user_id=user_id).first()
    
    if not channel:
        return {'error': 'Channel not found'}, 404
    
    db.session.delete(channel)
    db.session.commit()
    
    return {'message': 'Channel deleted successfully'}, 200
