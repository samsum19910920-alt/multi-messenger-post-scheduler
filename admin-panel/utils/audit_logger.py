from datetime import datetime
import json
import os

"""
Audit Logging برای ثبت تمام عملیات حساس
"""

LOG_FILE = 'admin_audit.log'

def log_action(action_type, user_id, description, ip_address, status='success'):
    """
    ثبت عملیات حساس
    
    action_type: delete_user, delete_channel, update_subscription, etc.
    user_id: کاربری که عملیات روی آن انجام شد
    description: توضیح عملیات
    ip_address: IP مدیر
    status: موفق یا ناموفق
    """
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action_type': action_type,
        'user_id': user_id,
        'description': description,
        'ip_address': ip_address,
        'status': status
    }
    
    # Write to log file
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Error writing to audit log: {e}")
    
    print(f"[AUDIT] {action_type}: {description}")

def get_audit_logs(limit=100):
    """
    خواندن لاگ‌های نظارتی
    """
    logs = []
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    logs.append(json.loads(line))
    except Exception as e:
        print(f"Error reading audit log: {e}")
    
    return logs
