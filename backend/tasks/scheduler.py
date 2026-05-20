from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
from backend.app import db, app
from backend.models import ScheduledPost, Media
from backend.utils.messengers import get_messenger

scheduler = BackgroundScheduler()

def send_scheduled_posts():
    """
    Check and send scheduled posts
    """
    with app.app_context():
        now = datetime.utcnow()
        pending_posts = ScheduledPost.query.filter(
            ScheduledPost.scheduled_time <= now,
            ScheduledPost.is_sent == False
        ).all()
        
        for post in pending_posts:
            try:
                # Send to all associated channels
                for channel in post.channels:
                    messenger = get_messenger(channel.messenger_type, channel.bot_token)
                    
                    # Send message with media
                    if post.caption:
                        messenger.send_message(channel.channel_id, post.caption)
                    
                    # Send media files
                    for media in post.media:
                        if media.media_type == 'image':
                            messenger.send_photo(channel.channel_id, media.file_path, post.caption)
                        elif media.media_type == 'video':
                            messenger.send_video(channel.channel_id, media.file_path, post.caption)
                
                # Mark as sent
                post.is_sent = True
                post.sent_at = datetime.utcnow()
                db.session.commit()
            
            except Exception as e:
                print(f"Error sending post {post.id}: {str(e)}")
                db.session.rollback()

def cleanup_old_files():
    """
    Delete files older than specified days
    """
    with app.app_context():
        days = int(os.getenv('AUTO_DELETE_AFTER_DAYS', 7))
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_media = Media.query.filter(Media.created_at < cutoff_date).all()
        
        for media in old_media:
            try:
                if os.path.exists(media.file_path):
                    os.remove(media.file_path)
                db.session.delete(media)
            except Exception as e:
                print(f"Error deleting file {media.file_path}: {str(e)}")
        
        db.session.commit()

def start_scheduler():
    """
    Start background scheduler
    """
    scheduler.add_job(send_scheduled_posts, 'interval', minutes=1)
    scheduler.add_job(cleanup_old_files, 'interval', hours=1)
    scheduler.start()
