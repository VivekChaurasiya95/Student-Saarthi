import uuid
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import declarative_base
from app import db

class User(db.Model):
    """Student / User model for authentication and profiling."""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    academic_percentage = db.Column(db.Float, nullable=True)
    field_of_study = db.Column(db.String(100), nullable=True)
    institution_name = db.Column(db.String(200), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    annual_income = db.Column(db.Integer, nullable=True)
    special_circumstances = db.Column(db.Text, nullable=True)
    profile_completion = db.Column(db.Integer, default=85)
    role = db.Column(db.String(20), default='student', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, raw_password: str) -> None:
        """Hash and set the user's password using PBKDF2/scrypt."""
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """
        Verify password against hash.
        Includes backward-compatibility check for legacy SHA256 hashes.
        If a legacy hash matches, automatically upgrade to secure Werkzeug hash.
        """
        if not self.password:
            return False
        
        # Check standard Werkzeug hash
        if self.password.startswith(('pbkdf2:', 'scrypt:', 'argon2:')):
            return check_password_hash(self.password, raw_password)
        
        # Legacy SHA256 check
        legacy_hash = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        if legacy_hash == self.password:
            # Upgrade password hash in place
            self.set_password(raw_password)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
            return True
            
        return False

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Serialize user object to dictionary for JSON responses."""
        data = {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'dob': self.dob.isoformat() if self.dob else None,
            'gender': self.gender,
            'address': self.address,
            'education_level': self.education_level,
            'academic_percentage': self.academic_percentage,
            'field_of_study': self.field_of_study,
            'institution_name': self.institution_name,
            'graduation_year': self.graduation_year,
            'category': self.category,
            'annual_income': self.annual_income,
            'special_circumstances': self.special_circumstances,
            'profile_completion': self.profile_completion,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_sensitive:
            data['password'] = self.password
        return data


class Admin(db.Model):
    """Admin user model for portal management."""
    __tablename__ = 'admins'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password: str) -> None:
        """Hash and set admin password."""
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verify admin password with legacy SHA256 migration support."""
        if not self.password:
            return False
            
        if self.password.startswith(('pbkdf2:', 'scrypt:', 'argon2:')):
            return check_password_hash(self.password, raw_password)
            
        legacy_hash = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        if legacy_hash == self.password:
            self.set_password(raw_password)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
            return True
            
        return False

    def to_dict(self) -> dict:
        """Serialize admin to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

