from backend.app import db
from datetime import datetime

class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('scheduled_posts.id'), nullable=False, index=True)
    file_path = db.Column(db.String(500), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)  # image, video
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'media_type': self.media_type,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'created_at': self.created_at.isoformat()
        }
