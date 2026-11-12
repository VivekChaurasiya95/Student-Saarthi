from datetime import datetime, date
from app import db

class Scholarship(db.Model):
    """Scholarship model storing official opportunity details."""
    __tablename__ = 'scholarships'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    min_percentage = db.Column(db.Float, default=0.0)
    education_levels = db.Column(db.Text, nullable=True)     # comma-separated string
    eligible_categories = db.Column(db.Text, nullable=True)  # comma-separated string
    max_income = db.Column(db.Integer, nullable=True)
    age_limit = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    deadline = db.Column(db.Date, nullable=True, index=True)
    application_procedure = db.Column(db.Text, nullable=True)
    official_url = db.Column(db.String(500), nullable=True)
    official_source = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=True)
    last_verified_date = db.Column(db.Date, default=date.today)
    required_documents = db.Column(db.Text, nullable=True)   # comma-separated string
    status = db.Column(db.String(20), default='active', index=True)
    max_applicants = db.Column(db.Integer, nullable=True)
    current_applicants = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serialize scholarship to dictionary matching existing frontend expectations."""
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'amount': float(self.amount) if self.amount is not None else 0.0,
            'category': self.category,
            'description': self.description or '',
            'min_percentage': float(self.min_percentage) if self.min_percentage is not None else 0.0,
            'education_levels': self.education_levels or '',
            'eligible_categories': self.eligible_categories or '',
            'max_income': self.max_income,
            'age_limit': self.age_limit,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'application_procedure': self.application_procedure or '',
            'official_url': self.official_url or '',
            'official_source': self.official_source or '',
            'is_verified': bool(self.is_verified),
            'last_verified_date': self.last_verified_date.isoformat() if self.last_verified_date else None,
            'required_documents': self.required_documents or '',
            'status': self.status,
            'max_applicants': self.max_applicants,
            'current_applicants': self.current_applicants,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

