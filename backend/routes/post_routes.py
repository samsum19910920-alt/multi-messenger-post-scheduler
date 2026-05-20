from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models import User, ScheduledPost, Media
from werkzeug.utils import secure_filename
import os
from datetime import datetime

post_bp = Blueprint('post', __name__, url_prefix='/api/posts')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    """Get all scheduled posts for current user"""
    user_id = get_jwt_identity()
    posts = ScheduledPost.query.filter_by(user_id=user_id).all()
    
    return {
        'posts': [p.to_dict() for p in posts]
    }, 200

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    """Create new scheduled post"""
    user_id = get_jwt_identity()
    
    caption = request.form.get('caption', '')
    scheduled_time_str = request.form.get('scheduled_time')
    post_type = request.form.get('post_type', 'text')
    
    if not scheduled_time_str:
        return {'error': 'scheduled_time is required'}, 400
    
    try:
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
    except ValueError:
        return {'error': 'Invalid scheduled_time format'}, 400
    
    post = ScheduledPost(
        user_id=user_id,
        caption=caption,
        post_type=post_type,
        scheduled_time=scheduled_time
    )
    
    # Handle file uploads
    if 'files' in request.files:
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(os.getenv('STORAGE_PATH', '/tmp/media'), filename)
                file.save(filepath)
                
                media = Media(
                    post=post,
                    file_path=filepath,
                    media_type='image' if filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'} else 'video',
                    file_size=os.path.getsize(filepath),
                    mime_type=file.content_type
                )
                db.session.add(media)
    
    db.session.add(post)
    db.session.commit()
    
    return post.to_dict(), 201

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete scheduled post"""
    user_id = get_jwt_identity()
    post = ScheduledPost.query.filter_by(id=post_id, user_id=user_id).first()
    
    if not post:
        return {'error': 'Post not found'}, 404
    
    db.session.delete(post)
    db.session.commit()
    
    return {'message': 'Post deleted successfully'}, 200
