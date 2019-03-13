from django.conf import settings
from datetime import datetime, timezone

def passwordIsExpired(user):
    # Password expiration not set
    if not hasattr(settings, 'PASSWORD_CHANGE_FREQUENCY') or not settings.PASSWORD_CHANGE_FREQUENCY:
        return False
        
    if (
        user.last_password_change and isinstance(user.last_password_change, datetime) and
        (datetime.now(timezone.utc) - user.last_password_change).total_seconds() < settings.PASSWORD_CHANGE_FREQUENCY
    ):
        return False
    else:
        return True
    
