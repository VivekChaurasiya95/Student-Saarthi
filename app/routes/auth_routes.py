from flask import Blueprint, render_template, request, jsonify, session, current_app
from app.services.auth_service import AuthService
from app.utils.validators import validate_registration_data

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
@auth_bp.route('/login.html')
def login_page():
    """Render unified login page."""
    client_id = current_app.config.get('GOOGLE_CLIENT_ID', '1080666056729-ameupnthncvtjko6lgo2u0237n46ggq7.apps.googleusercontent.com')
    return render_template('pages/login.html', google_client_id=client_id)

@auth_bp.route('/signup')
@auth_bp.route('/signup.html')
def signup_page():
    """Render student registration page."""
    return render_template('pages/signup.html')

# ==================== AUTHENTICATION API ENDPOINTS ====================

@auth_bp.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    """Register a new student."""
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json(silent=True) or request.form.to_dict()
    is_valid, err_msg = validate_registration_data(data)
    if not is_valid:
        return jsonify({'error': err_msg}), 400

    success, user_dict, message = AuthService.register_user(data)
    if not success:
        return jsonify({'error': message}), 400

    # Establish authenticated session
    session.permanent = True
    session['user_id'] = user_dict['id']
    session['user_name'] = user_dict['full_name']
    session['user_role'] = 'student'

    return jsonify({
        'success': True,
        'userId': user_dict['id'],
        'message': message
    }), 201

@auth_bp.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    """Authenticate student user."""
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json(silent=True) or request.form.to_dict()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    success, user_dict, message = AuthService.login_user(email, password)
    if not success:
        return jsonify({'error': message}), 401

    session.permanent = True
    session['user_id'] = user_dict['id']
    session['user_name'] = user_dict['full_name']
    session['user_role'] = 'student'

    return jsonify({
        'success': True,
        'userId': user_dict['id'],
        'userName': user_dict['full_name']
    }), 200

@auth_bp.route('/api/admin/login', methods=['POST', 'OPTIONS'])
def admin_login():
    """Authenticate portal administrator."""
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json(silent=True) or request.form.to_dict()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    success, admin_dict, message = AuthService.login_admin(username, password)
    if not success:
        return jsonify({'error': message}), 401

    session.permanent = True
    session['admin_id'] = admin_dict['id']
    session['admin_username'] = admin_dict['username']
    session['user_role'] = 'admin'

    return jsonify({
        'success': True,
        'adminId': admin_dict['id'],
        'username': admin_dict['username']
    }), 200

@auth_bp.route('/api/logout', methods=['POST', 'GET', 'OPTIONS'])
def logout():
    """Log out current user or administrator."""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/check-session', methods=['GET', 'OPTIONS'])
def check_session():
    """Verify active session credentials."""
    if 'user_id' in session:
        return jsonify({
            'loggedIn': True,
            'userId': session['user_id'],
            'userName': session.get('user_name'),
            'type': 'user'
        }), 200
    elif 'admin_id' in session:
        return jsonify({
            'loggedIn': True,
            'adminId': session['admin_id'],
            'username': session.get('admin_username'),
            'type': 'admin'
        }), 200
    else:
        return jsonify({'loggedIn': False}), 200

@auth_bp.route('/api/auth/google', methods=['POST'])
def google_auth():
    """Handle Google OAuth credential exchange."""
    data = request.get_json(silent=True) or {}
    if not data.get('token') and not data.get('email'):
        return jsonify({'error': 'Google token or email is required'}), 400

    google_user = {
        'email': data.get('email'),
        'name': data.get('name', 'Google User'),
        'google_id': data.get('google_id')
    }

    success, user_dict, message = AuthService.google_auth(google_user)
    if not success:
        return jsonify({'error': message}), 500

    session.permanent = True
    session['user_id'] = user_dict['id']
    session['user_name'] = user_dict['full_name']
    session['user_role'] = 'student'

    return jsonify({
        'success': True,
        'userId': user_dict['id'],
        'userName': user_dict['full_name'],
        'message': message
    }), 200

