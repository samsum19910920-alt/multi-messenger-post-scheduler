from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.getenv('DEBUG', False)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24)))

# CORS Configuration
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    }
})

# Database
db = SQLAlchemy(app)

# JWT Manager
jwt = JWTManager(app)

# Import models and routes
from backend.models import User, Channel, ScheduledPost, Media
from backend.routes import auth_routes, user_routes, channel_routes, post_routes, admin_routes

# Register blueprints
app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(channel_routes.channel_bp)
app.register_blueprint(post_routes.post_bp)
app.register_blueprint(admin_routes.admin_bp)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('DEBUG', False), host='0.0.0.0', port=5000)
