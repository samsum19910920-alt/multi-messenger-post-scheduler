import re

def validate_phone_number(phone_number):
    """
    Validate Iranian phone number
    """
    # Iranian phone numbers start with 09 and have 11 digits
    pattern = r'^09\d{9}$'
    return re.match(pattern, phone_number) is not None

def validate_password(password):
    """
    Validate password strength
    - At least 8 characters
    - Contains letters and numbers
    """
    if len(password) < 8:
        return False
    
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_letter and has_digit

def validate_channel_data(data):
    """
    Validate channel data
    """
    required_fields = ['messenger_type', 'channel_id', 'bot_token']
    valid_messengers = ['rubika', 'bale', 'eitaa', 'soroosh']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    
    if data['messenger_type'] not in valid_messengers:
        return False
    
    return True
