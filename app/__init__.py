import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, Date, DateTime,
    Boolean, ForeignKey, UniqueConstraint, Index, or_, and_, text
)
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship, backref

class SQLAlchemy:
    """Lightweight SQLAlchemy integration adhering to Flask patterns."""
    Column = Column
    Integer = Integer
    String = String
    Text = Text
    Float = Float
    Date = Date
    DateTime = DateTime
    Boolean = Boolean
    ForeignKey = ForeignKey
    UniqueConstraint = UniqueConstraint
    Index = Index
    relationship = staticmethod(relationship)
    backref = staticmethod(backref)
    text = staticmethod(text)
    or_ = staticmethod(or_)
    and_ = staticmethod(and_)

    def __init__(self, app=None):
        self.Model = declarative_base()
        self.engine = None
        self.session_factory = None
        self.session = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///instance/database/student_saarthi.db')
        connect_args = {}
        if db_uri.startswith('sqlite'):
            connect_args['check_same_thread'] = False
            
        self.engine = create_engine(db_uri, connect_args=connect_args)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.session_factory)
        self.Model.query = self.session.query_property()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            self.session.remove()

    def create_all(self):
        if self.engine is not None:
            self.Model.metadata.create_all(bind=self.engine)

    def drop_all(self):
        if self.engine is not None:
            self.Model.metadata.drop_all(bind=self.engine)

# Core extensions instances
db = SQLAlchemy()
cors = CORS()

def create_app(config_class=None):
    """
    Application Factory Pattern for Student Saarthi.
    Configures and assembles Flask blueprints, database, security, and logging.
    """
    from app.config import config_by_name, DevelopmentConfig
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(basedir, '..'))

    # Determine configuration class
    if isinstance(config_class, str):
        config_class = config_by_name.get(config_class.lower(), DevelopmentConfig)
    elif config_class is None:
        env_mode = os.environ.get('FLASK_ENV', 'development').lower()
        config_class = config_by_name.get(env_mode, DevelopmentConfig)

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder=os.path.join(project_root, 'static'),
        static_url_path='/static'
    )
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    cors.init_app(
        app,
        supports_credentials=True,
        origins=app.config.get('CORS_ORIGINS', ['*']),
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Ensure required runtime directories exist
    os.makedirs(os.path.join(project_root, 'instance', 'database'), exist_ok=True)
    os.makedirs(app.config.get('UPLOAD_FOLDER', os.path.join(project_root, 'static', 'documents', 'uploads')), exist_ok=True)
    os.makedirs(os.path.join(project_root, 'logs'), exist_ok=True)

    # Setup Logging
    if not app.debug or os.environ.get('FORCE_FILE_LOGGING'):
        log_file = app.config.get('LOG_FILE', os.path.join(project_root, 'logs', 'app.log'))
        file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Student Saarthi initialized with Application Factory')

    # Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.scholarship_routes import scholarship_bp
    from app.routes.application_routes import application_bp
    from app.routes.student_routes import student_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.contact_routes import contact_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(scholarship_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(contact_bp)

    # Auto-initialize database tables and seed if empty in non-testing environments
    if not app.testing:
        with app.app_context():
            try:
                db.create_all()
                from app.models.scholarship import Scholarship
                if Scholarship.query.count() == 0:
                    from scripts.seed_db import seed_database
                    seed_database(app=app)
            except Exception as e:
                app.logger.warning(f"Database auto-init skipped or failed: {e}")

    # Register Error Handlers
    @app.errorhandler(404)
    def handle_not_found(error):
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({'error': 'Resource not found'}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def handle_forbidden(error):
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({'error': 'Forbidden access'}), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def handle_server_error(error):
        app.logger.error(f'Internal Server Error: {error}')
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500

    # Prevent caching of static assets in development to avoid 304 / stale files
    @app.after_request
    def add_cache_headers(response):
        if app.debug or app.config.get('SEND_FILE_MAX_AGE_DEFAULT') == 0:
            if request.path.startswith('/static/'):
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
        return response

    # Auto-create tables on startup
    with app.app_context():
        db.create_all()

    return app
