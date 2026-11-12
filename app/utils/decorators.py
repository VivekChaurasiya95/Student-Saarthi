from functools import wraps
from flask import session, jsonify, request, redirect, url_for

def login_required(f):
    """Ensure user is logged in as student."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Check if API request or JSON requested
            if request.path.startswith('/api/') or request.is_json or request.headers.get('Accept') == 'application/json':
                return jsonify({'error': 'Authentication required'}), 401
            return redirect('/login.html')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Ensure user is logged in as administrator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            # Check if API request or JSON requested
            if request.path.startswith('/api/') or request.is_json or request.headers.get('Accept') == 'application/json':
                return jsonify({'error': 'Admin authentication required'}), 401
            return redirect('/login.html?admin=true')
        return f(*args, **kwargs)
    return decorated_function

