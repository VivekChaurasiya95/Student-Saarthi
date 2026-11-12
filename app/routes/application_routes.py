import os
from flask import Blueprint, render_template, request, jsonify, session, current_app
from app.utils.decorators import login_required
from app.utils.validators import allowed_file
from app.utils.helpers import save_uploaded_file
from app.services.application_service import ApplicationService

application_bp = Blueprint('applications', __name__)

@application_bp.route('/apply')
@application_bp.route('/applyscholarship.html')
@login_required
def apply_page():
    """Render scholarship application form."""
    return render_template('pages/apply.html')

@application_bp.route('/my-applications')
@application_bp.route('/my-application.html')
@login_required
def my_applications_page():
    """Render student's submitted applications dashboard."""
    return render_template('pages/my_applications.html')

# ==================== APPLICATION API ENDPOINTS ====================

@application_bp.route('/api/apply', methods=['POST'])
@login_required
def submit_application():
    """Submit scholarship application with optional document attachments."""
    user_id = session.get('user_id')
    
    # Handle both multipart/form-data and application/json
    is_multipart = request.content_type and 'multipart/form-data' in request.content_type
    if is_multipart:
        data = request.form.to_dict()
    else:
        data = request.get_json(silent=True) or {}

    scholarship_id = data.get('scholarshipId') or data.get('scholarship_id')
    if not scholarship_id:
        return jsonify({'error': 'Scholarship ID is required'}), 400

    try:
        scholarship_id = int(scholarship_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid scholarship ID'}), 400

    sop = data.get('sop', '').strip()
    if len(sop) < 50: # Standard validation
        return jsonify({'error': 'Statement of purpose must be at least 50 characters long'}), 400

    achievements = data.get('achievements', '').strip()
    extracurricular = data.get('extracurricular', '').strip()
    additional_info = data.get('additionalInfo', '').strip()

    # Handle document file uploads if present
    documents_metadata = []
    if is_multipart and 'documents' in request.files:
        files = request.files.getlist('documents')
        upload_base = current_app.config['UPLOAD_FOLDER']
        allowed_exts = current_app.config['ALLOWED_EXTENSIONS']

        for file_obj in files:
            if file_obj and file_obj.filename != '':
                if allowed_file(file_obj.filename, allowed_exts):
                    fname, fpath, fsize = save_uploaded_file(file_obj, upload_base, subfolder='applications')
                    doc_type = data.get('documentType', 'Supporting Document')
                    documents_metadata.append({
                        'document_type': doc_type,
                        'file_name': fname,
                        'file_path': fpath,
                        'file_size': fsize
                    })

    success, app_dict, message = ApplicationService.apply(
        user_id=user_id,
        scholarship_id=scholarship_id,
        statement_of_purpose=sop,
        achievements=achievements,
        extracurricular=extracurricular,
        additional_info=additional_info,
        documents=documents_metadata
    )

    if not success:
        return jsonify({'error': message}), 400

    return jsonify({
        'success': True,
        'applicationId': app_dict['id'],
        'message': message
    }), 201

@application_bp.route('/api/applications', methods=['GET'])
@login_required
def get_student_applications():
    """Fetch applications submitted by authenticated student."""
    user_id = session.get('user_id')
    try:
        applications = ApplicationService.get_student_applications(user_id)
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch applications: {str(e)}'}), 500

