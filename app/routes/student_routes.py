from flask import Blueprint, render_template, request, jsonify, session
from app.utils.decorators import login_required
from app.services.auth_service import AuthService
from app.services.application_service import ApplicationService
from app.services.notification_service import NotificationService

student_bp = Blueprint('student', __name__)

@student_bp.route('/student/dashboard')
@student_bp.route('/student-dashboard.html')
@login_required
def dashboard():
    """Render student dashboard."""
    return render_template('pages/student_dashboard.html')

# ==================== STUDENT API ENDPOINTS ====================

@student_bp.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    """Get or update authenticated student's profile."""
    user_id = session.get('user_id')

    if request.method == 'GET':
        profile_data = AuthService.get_user_profile(user_id)
        if profile_data:
            return jsonify(profile_data), 200
        return jsonify({'error': 'User not found'}), 404

    # PUT update profile
    data = request.get_json(silent=True) or request.form.to_dict()
    success, updated_user, message = AuthService.update_user_profile(user_id, data)
    if success:
        return jsonify(updated_user), 200
    return jsonify({'error': message}), 400

@student_bp.route('/api/bookmarks', methods=['GET', 'POST'])
@login_required
def bookmarks():
    """Retrieve or add scholarship bookmarks."""
    user_id = session.get('user_id')

    if request.method == 'GET':
        try:
            saved_list = ApplicationService.get_student_bookmarks(user_id)
            return jsonify(saved_list), 200
        except Exception as e:
            return jsonify({'error': f'Failed to fetch bookmarks: {str(e)}'}), 500

    # POST add bookmark
    data = request.get_json(silent=True) or request.form.to_dict()
    scholarship_id = data.get('scholarshipId') or data.get('scholarship_id')

    if not scholarship_id:
        return jsonify({'error': 'Scholarship ID is required'}), 400

    try:
        scholarship_id = int(scholarship_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid scholarship ID'}), 400

    success, message = ApplicationService.add_bookmark(user_id, scholarship_id)
    if success:
        return jsonify({'success': True, 'message': message}), 201
    return jsonify({'error': message}), 400

@student_bp.route('/api/bookmarks/<int:scholarship_id>', methods=['DELETE'])
@login_required
def delete_bookmark(scholarship_id):
    """Remove a bookmarked scholarship."""
    user_id = session.get('user_id')
    success, message = ApplicationService.remove_bookmark(user_id, scholarship_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'error': message}), 404

@student_bp.route('/api/notifications', methods=['GET'])
@login_required
def notifications():
    """Retrieve student notifications."""
    user_id = session.get('user_id')
    notifs = NotificationService.get_user_notifications(user_id)
    return jsonify(notifs), 200

