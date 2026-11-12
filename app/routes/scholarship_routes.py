from flask import Blueprint, render_template, request, jsonify
from app.services.scholarship_service import ScholarshipService

scholarship_bp = Blueprint('scholarships', __name__)

@scholarship_bp.route('/scholarships')
@scholarship_bp.route('/scholarships.html')
def browse_scholarships():
    """Render scholarship discovery directory page."""
    return render_template('pages/scholarships.html')

@scholarship_bp.route('/scholarships/<int:scholarship_id>')
def scholarship_detail(scholarship_id):
    """Render detailed scholarship view."""
    scholarship = ScholarshipService.get_by_id(scholarship_id)
    if not scholarship:
        return render_template('errors/404.html', message="Scholarship not found"), 404
    return render_template('pages/scholarship_detail.html', scholarship=scholarship)

# ==================== SCHOLARSHIP API ENDPOINTS ====================

@scholarship_bp.route('/api/scholarships', methods=['GET'])
def get_scholarships():
    """Get active scholarships with optional search and filter criteria."""
    search = request.args.get('search')
    category = request.args.get('category')
    education = request.args.get('education')
    
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)
    
    # Support 'amount' range format e.g. '25000-50000'
    amount_range = request.args.get('amount')
    if amount_range and '-' in amount_range:
        parts = amount_range.split('-')
        try:
            min_amount = float(parts[0])
            max_amount = float(parts[1])
        except ValueError:
            pass

    deadline_days = request.args.get('deadline', type=int)

    try:
        scholarships = ScholarshipService.get_all(
            status='active',
            search=search,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
            education_level=education,
            days_deadline=deadline_days
        )
        return jsonify(scholarships), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch scholarships: {str(e)}'}), 500

@scholarship_bp.route('/api/scholarships/featured', methods=['GET'])
def get_featured_scholarships():
    """Get featured scholarships for the homepage showcase."""
    try:
        limit = request.args.get('limit', default=6, type=int)
        featured = ScholarshipService.get_featured(limit=limit)
        return jsonify(featured), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch featured scholarships: {str(e)}'}), 500

@scholarship_bp.route('/api/scholarships/<int:scholarship_id>', methods=['GET'])
def get_scholarship(scholarship_id):
    """Fetch single scholarship details by ID."""
    try:
        scholarship = ScholarshipService.get_by_id(scholarship_id)
        if scholarship:
            return jsonify(scholarship), 200
        return jsonify({'error': 'Scholarship not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to fetch scholarship: {str(e)}'}), 500

