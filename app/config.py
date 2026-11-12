import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(basedir, '..'))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'student_saarthi_production_ready_secret_key_2026_982341'
    
    # Database Configuration
    # Defaults to SQLite in instance/database/student_saarthi.db
    # Supports MySQL or PostgreSQL via DATABASE_URL
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url:
        if _db_url.startswith('postgres://'):
            _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
        if _db_url.startswith('sqlite:///instance/'):
            # Resolve relative instance path to absolute path
            db_rel = _db_url.replace('sqlite:///instance/', '')
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(project_root, 'instance', db_rel)}"
        else:
            SQLALCHEMY_DATABASE_URI = _db_url
    else:
        db_path = os.path.join(project_root, 'instance', 'database', 'student_saarthi.db')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    SESSION_COOKIE_NAME = 'student_saarthi_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_REFRESH_EACH_REQUEST = True

    # CORS Settings
    CORS_ORIGINS = [
        "http://127.0.0.1:5000", "http://localhost:5000",
        "http://127.0.0.1:5500", "http://localhost:5500",
        "http://127.0.0.1:8000", "http://localhost:8000"
    ]

    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(project_root, 'static', 'documents', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB max
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

    # Logging
    LOG_FILE = os.path.join(project_root, 'logs', 'app.log')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '1080666056729-ameupnthncvtjko6lgo2u0237n46ggq7.apps.googleusercontent.com')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

