from flask import Blueprint, render_template, request, jsonify
from app.utils.decorators import admin_required
from app.utils.validators import validate_scholarship_data
from app.services.application_service import ApplicationService
from app.services.scholarship_service import ScholarshipService
from app.models.user import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_bp.route('/admin-dashboard.html')
@admin_required
def admin_dashboard():
    """Render admin management dashboard."""
    return render_template('pages/admin_dashboard.html')

# ==================== ADMIN API ENDPOINTS ====================

@admin_bp.route('/api/admin/applications', methods=['GET'])
@admin_required
def admin_get_applications():
    """Fetch all student applications for administrator review."""
    status = request.args.get('status')
    try:
        applications = ApplicationService.get_all_applications(status=status)
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch applications: {str(e)}'}), 500

@admin_bp.route('/api/admin/applications/<application_id>', methods=['PUT'])
@admin_required
def admin_update_application(application_id):
    """Update status and administrative feedback on an application."""
    data = request.get_json(silent=True) or request.form.to_dict()
    new_status = data.get('status')
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400

    admin_notes = data.get('notes') or data.get('admin_notes')
    success, updated_app, message = ApplicationService.update_status(
        application_id=application_id,
        new_status=new_status,
        admin_notes=admin_notes
    )

    if success:
        return jsonify({
            'success': True,
            'message': message,
            'application': updated_app
        }), 200
    return jsonify({'error': message}), 400

@admin_bp.route('/api/admin/scholarships', methods=['POST'])
@admin_required
def admin_add_scholarship():
    """Create a new scholarship entry."""
    data = request.get_json(silent=True) or request.form.to_dict()
    is_valid, err_msg = validate_scholarship_data(data)
    if not is_valid:
        return jsonify({'error': err_msg}), 400

    success, sch_dict, message = ScholarshipService.create(data)
    if success:
        return jsonify({
            'success': True,
            'scholarshipId': sch_dict['id'],
            'scholarship': sch_dict,
            'message': message
        }), 201
    return jsonify({'error': message}), 500

@admin_bp.route('/api/admin/scholarships/<int:scholarship_id>', methods=['PUT'])
@admin_required
def admin_update_scholarship(scholarship_id):
    """Modify details of an existing scholarship."""
    data = request.get_json(silent=True) or request.form.to_dict()
    success, sch_dict, message = ScholarshipService.update(scholarship_id, data)
    if success:
        return jsonify({
            'success': True,
            'scholarship': sch_dict,
            'message': message
        }), 200
    return jsonify({'error': message}), 400

@admin_bp.route('/api/admin/scholarships/<int:scholarship_id>', methods=['DELETE'])
@admin_required
def admin_delete_scholarship(scholarship_id):
    """Remove a scholarship from the system."""
    success, message = ScholarshipService.delete(scholarship_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'error': message}), 400

@admin_bp.route('/api/admin/users', methods=['GET'])
@admin_required
def admin_get_users():
    """List registered student accounts for administration."""
    try:
        users = (User.query
                 .filter_by(role='student')
                 .order_by(User.created_at.desc())
                 .all())
        users_data = [{
            'id': u.id,
            'full_name': u.full_name,
            'email': u.email,
            'phone': u.phone,
            'education_level': u.education_level,
            'category': u.category,
            'academic_percentage': u.academic_percentage,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in users]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch users: {str(e)}'}), 500

