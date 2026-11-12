import os
import sys
import pytest
from datetime import date

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.config import TestingConfig
from app.models.user import User, Admin
from app.models.scholarship import Scholarship

@pytest.fixture
def app():
    """Create and configure a clean testing application."""
    test_app = create_app(TestingConfig)
    with test_app.app_context():
        db.create_all()
        
        # Seed test admin
        admin = Admin(username='admin', email='admin@studentsaarthi.com')
        admin.set_password('admin123')
        db.session.add(admin)

        # Seed test scholarship
        sch = Scholarship(
            id=1,
            name='Test National Scholarship',
            provider='Test Ministry',
            amount=50000.0,
            category='Academic',
            description='Test scholarship description for unit tests.',
            min_percentage=60.0,
            education_levels='Undergraduate,Postgraduate',
            eligible_categories='General,OBC,SC-ST',
            max_income=500000,
            deadline=date(2026, 12, 31),
            status='active',
            max_applicants=100,
            current_applicants=0,
            is_verified=True
        )
        db.session.add(sch)
        db.session.commit()

        yield test_app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for HTTP requests."""
    return app.test_client()

@pytest.fixture
def student_auth_client(app, client):
    """Client with authenticated student session."""
    with app.app_context():
        user = User(
            full_name='Test Student',
            email='student@example.com',
            phone='9876543210',
            education_level='Undergraduate',
            academic_percentage=85.0,
            category='General',
            annual_income=300000,
            role='student'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['user_name'] = 'Test Student'
        sess['user_role'] = 'student'

    return client

@pytest.fixture
def admin_auth_client(app, client):
    """Client with authenticated admin session."""
    with app.app_context():
        admin = Admin.query.filter_by(username='admin').first()
        admin_id = admin.id

    with client.session_transaction() as sess:
        sess['admin_id'] = admin_id
        sess['admin_username'] = 'admin'
        sess['user_role'] = 'admin'

    return client

