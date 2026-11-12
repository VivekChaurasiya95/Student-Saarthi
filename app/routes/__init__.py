from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.scholarship_routes import scholarship_bp
from app.routes.application_routes import application_bp
from app.routes.student_routes import student_bp
from app.routes.admin_routes import admin_bp
from app.routes.contact_routes import contact_bp

__all__ = [
    'main_bp',
    'auth_bp',
    'scholarship_bp',
    'application_bp',
    'student_bp',
    'admin_bp',
    'contact_bp'
]

