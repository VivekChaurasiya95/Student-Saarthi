from datetime import datetime
from flask import Blueprint, render_template, jsonify
from app import db
from app.services.scholarship_service import ScholarshipService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index.html')
def home():
    """Render public homepage."""
    return render_template('pages/index.html')

@main_bp.route('/about')
@main_bp.route('/about.html')
def about():
    """Render About Us page."""
    return render_template('pages/about.html')

@main_bp.route('/contact')
@main_bp.route('/contact.html')
def contact():
    """Render Contact Us page."""
    return render_template('pages/contact.html')

@main_bp.route('/help')
@main_bp.route('/helpCentre.html')
def help_centre():
    """Render Help & FAQ page."""
    return render_template('pages/help.html')

@main_bp.route('/privacy')
@main_bp.route('/PrivacyPolicy.html')
def privacy_policy():
    """Render Privacy Policy page."""
    return render_template('pages/privacy.html')

@main_bp.route('/terms')
@main_bp.route('/termOfServices.html')
def terms_of_service():
    """Render Terms of Service page."""
    return render_template('pages/terms.html')

@main_bp.route('/developers')
@main_bp.route('/developers.html')
def developers():
    """Render Developers & Engineering Team page."""
    return render_template('pages/developers.html')

# ==================== PUBLIC API ENDPOINTS ====================

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """Check API health and database connectivity."""
    db_status = 'disconnected'
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception:
        db_status = 'error'

    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@main_bp.route('/api/stats', methods=['GET'])
def portal_stats():
    """Return aggregated portal statistics."""
    try:
        stats = ScholarshipService.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch statistics: {str(e)}'}), 500

