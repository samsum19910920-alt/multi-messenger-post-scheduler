from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.app import db
from backend.models import User
from backend.utils.otp import send_otp, verify_otp
from backend.utils.validators import validate_phone_number, validate_password
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/send-otp', methods=['POST'])
def send_otp_endpoint():
    """Send OTP to phone number"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number or not validate_phone_number(phone_number):
        return {'error': 'Invalid phone number'}, 400
    
    try:
        result = send_otp(phone_number)
        if result['success']:
            return {'message': 'OTP sent successfully'}, 200
        else:
            return {'error': result.get('error', 'Failed to send OTP')}, 500
    except Exception as e:
        return {'error': str(e)}, 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp_endpoint():
    """Verify OTP and create/login user"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    otp_code = data.get('otp_code')
    password = data.get('password')  # For new users
    
    if not phone_number or not otp_code:
        return {'error': 'Missing required fields'}, 400
    
    # Verify OTP
    if not verify_otp(phone_number, otp_code):
        return {'error': 'Invalid or expired OTP'}, 401
    
    # Check if user exists
    user = User.query.filter_by(phone_number=phone_number).first()
    
    if not user:
        # Create new user
        if not password or not validate_password(password):
            return {'error': 'Invalid password'}, 400
        
        user = User(phone_number=phone_number)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    
    # Create JWT token
    access_token = create_access_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'user': user.to_dict()
    }, 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return user.to_dict(), 200
