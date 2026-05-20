from backend.app import db
from datetime import datetime

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    messenger_type = db.Column(db.String(50), nullable=False)  # rubika, bale, eitaa, soroosh
    channel_id = db.Column(db.String(255), nullable=False)
    channel_name = db.Column(db.String(255), nullable=True)
    channel_username = db.Column(db.String(255), nullable=True)
    bot_token = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scheduled_posts = db.relationship('ScheduledPost', secondary='post_channels', backref='channels')
    
    def to_dict(self):
        return {
            'id': self.id,
            'messenger_type': self.messenger_type,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'channel_username': self.channel_username,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
