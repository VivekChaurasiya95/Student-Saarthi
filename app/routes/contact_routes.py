from flask import Blueprint, request, jsonify
from app.services.notification_service import NotificationService
from app.utils.validators import validate_email

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle public contact inquiries."""
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name') or data.get('fullName')
    email = data.get('email')
    subject = data.get('subject', 'General Inquiry')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message are required'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email address format'}), 400

    success, reply = NotificationService.save_contact(name, email, subject, message)
    if success:
        return jsonify({'success': True, 'message': reply}), 201
    return jsonify({'error': reply}), 500

