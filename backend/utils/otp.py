import os
import requests
from datetime import datetime, timedelta
import random
from functools import lru_cache

# In-memory OTP storage (for development)
# In production, use Redis or database
otp_storage = {}

def send_otp(phone_number):
    """
    Send OTP via Faraz SMS
    """
    try:
        # Generate random 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Store OTP with expiration (5 minutes)
        otp_storage[phone_number] = {
            'code': otp_code,
            'expires_at': datetime.utcnow() + timedelta(minutes=int(os.getenv('OTP_EXPIRATION_MINUTES', 5))),
            'attempts': 0
        }
        
        # Send via Faraz SMS
        api_url = os.getenv('FARAZ_SMS_API_URL')
        api_key = os.getenv('FARAZ_SMS_API_KEY')
        
        # Example payload for Faraz SMS
        payload = {
            'api_key': api_key,
            'to': phone_number,
            'message': f'کد تایید شما: {otp_code}'
        }
        
        # In development, just log it
        if os.getenv('FLASK_ENV') == 'development':
            print(f'[DEBUG] OTP for {phone_number}: {otp_code}')
            return {'success': True}
        
        # In production, send via API
        response = requests.post(f'{api_url}send', data=payload, timeout=10)
        
        if response.status_code == 200:
            return {'success': True}
        else:
            return {'success': False, 'error': 'Failed to send SMS'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

def verify_otp(phone_number, otp_code):
    """
    Verify OTP code
    """
    if phone_number not in otp_storage:
        return False
    
    otp_data = otp_storage[phone_number]
    
    # Check expiration
    if datetime.utcnow() > otp_data['expires_at']:
        del otp_storage[phone_number]
        return False
    
    # Check attempts
    if otp_data['attempts'] >= int(os.getenv('OTP_MAX_ATTEMPTS', 3)):
        del otp_storage[phone_number]
        return False
    
    # Verify code
    if otp_data['code'] == otp_code:
        del otp_storage[phone_number]
        return True
    
    otp_data['attempts'] += 1
    return False
