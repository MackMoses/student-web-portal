from functools import wraps
from flask_login import current_user
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Add your admin check logic here
        # For example:
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return "You don't have permission to access this page", 403
    return decorated_function