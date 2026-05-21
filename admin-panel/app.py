from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__, template_folder='admin-panel/templates', static_folder='admin-panel/static')
app.secret_key = os.getenv('SECRET_KEY', 'admin-secret-key-change-in-production')

CORS(app)

# Admin credentials (in production, use database)
ADMIN_KEY = os.getenv('ADMIN_PASSWORD_HASH', 'admin123')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')

# Decorator برای احراز هویت Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_key = request.headers.get('X-Admin-Key')
        
        if not admin_key or admin_key != ADMIN_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# Home Route
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

# Dashboard
@app.route('/admin/dashboard')
def dashboard():
    """صفحه داشبورد - نمایش آمار و گزارش‌ها"""
    return render_template('dashboard.html')

# API Routes - Users
@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    """دریافت لیست تمام کاربران"""
    try:
        # This would fetch from the main backend
        import requests
        response = requests.get('http://localhost:5000/api/admin/users',
                             headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """دریافت اطلاعات کاربر خاص"""
    try:
        import requests
        response = requests.get(f'http://localhost:5000/api/user/profile',
                             headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """حذف کاربر"""
    try:
        # Log the deletion
        log_audit('delete_user', f'User {user_id} deleted', request.remote_addr)
        
        import requests
        response = requests.delete(f'http://localhost:5000/api/admin/users/{user_id}',
                                 headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>/subscription', methods=['POST'])
@admin_required
def update_subscription(user_id):
    """تمدید اشتراک کاربر"""
    try:
        data = request.get_json()
        
        # Log the subscription update
        log_audit('update_subscription', 
                 f'User {user_id} subscription updated to {data.get("subscription_end")}',
                 request.remote_addr)
        
        import requests
        response = requests.post(f'http://localhost:5000/api/admin/users/{user_id}/subscription',
                               headers={'X-Admin-Key': ADMIN_KEY},
                               json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Routes - Statistics
@app.route('/api/admin/statistics', methods=['GET'])
@admin_required
def get_statistics():
    """دریافت آمار سیستم"""
    try:
        import requests
        response = requests.get('http://localhost:5000/api/admin/statistics',
                             headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Routes - Channels
@app.route('/api/admin/channels', methods=['GET'])
@admin_required
def get_all_channels():
    """دریافت لیست تمام کاناله‌ها"""
    try:
        import requests
        response = requests.get('http://localhost:5000/api/channels/',
                             headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/channels/<int:channel_id>', methods=['DELETE'])
@admin_required
def delete_channel(channel_id):
    """حذف کانال"""
    try:
        log_audit('delete_channel', f'Channel {channel_id} deleted', request.remote_addr)
        
        import requests
        response = requests.delete(f'http://localhost:5000/api/channels/{channel_id}',
                                 headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Routes - Posts
@app.route('/api/admin/posts', methods=['GET'])
@admin_required
def get_all_posts():
    """دریافت لیست تمام پست‌ها"""
    try:
        import requests
        response = requests.get('http://localhost:5000/api/posts/',
                             headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/posts/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_post(post_id):
    """حذف پست"""
    try:
        log_audit('delete_post', f'Post {post_id} deleted', request.remote_addr)
        
        import requests
        response = requests.delete(f'http://localhost:5000/api/posts/{post_id}',
                                 headers={'X-Admin-Key': ADMIN_KEY})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Audit Logging
audit_logs = []  # In production, use database

def log_audit(action, description, ip_address):
    """ثبت عملیات حساس"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': action,
        'description': description,
        'ip_address': ip_address,
        'status': 'success'
    }
    audit_logs.append(log_entry)
    print(f"[AUDIT] {action}: {description} from {ip_address}")

@app.route('/api/admin/logs', methods=['GET'])
@admin_required
def get_audit_logs():
    """دریافت لاگ فعالیت‌ها"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Paginate logs
        start = (page - 1) * per_page
        end = start + per_page
        
        return jsonify({
            'logs': audit_logs[start:end],
            'total': len(audit_logs),
            'page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', False), host='0.0.0.0', port=5001)
