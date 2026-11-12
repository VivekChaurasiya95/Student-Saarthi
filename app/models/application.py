import uuid
from datetime import datetime
from app import db

class Application(db.Model):
    """Application submitted by a student for a specific scholarship."""
    __tablename__ = 'applications'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id', ondelete='CASCADE'), nullable=False, index=True)
    application_status = db.Column(db.String(50), default='Submitted', nullable=False, index=True)
    statement_of_purpose = db.Column(db.Text, nullable=True)
    academic_achievements = db.Column(db.Text, nullable=True)
    extracurricular_activities = db.Column(db.Text, nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_notes = db.Column(db.Text, nullable=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('applications', lazy=True, cascade='all, delete-orphan'))
    scholarship = db.relationship('Scholarship', backref=db.backref('applications', lazy=True, cascade='all, delete-orphan'))
    documents = db.relationship('ApplicationDocument', backref='application', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_relations: bool = True) -> dict:
        """Serialize application to dictionary format."""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'scholarship_id': self.scholarship_id,
            'application_status': self.application_status,
            'statement_of_purpose': self.statement_of_purpose or '',
            'academic_achievements': self.academic_achievements or '',
            'extracurricular_activities': self.extracurricular_activities or '',
            'additional_info': self.additional_info or '',
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'admin_notes': self.admin_notes or ''
        }
        if include_relations:
            if self.scholarship:
                data['scholarship_name'] = self.scholarship.name
                data['amount'] = float(self.scholarship.amount)
                data['provider'] = self.scholarship.provider
                data['deadline'] = self.scholarship.deadline.isoformat() if self.scholarship.deadline else None
            if self.user:
                data['student_name'] = self.user.full_name
                data['student_email'] = self.user.email
                data['student_phone'] = self.user.phone
                data['education_level'] = self.user.education_level
                data['category'] = self.user.category
                data['academic_percentage'] = self.user.academic_percentage
            data['documents'] = [doc.to_dict() for doc in self.documents] if self.documents else []
        return data


class ApplicationDocument(db.Model):
    """Uploaded verification documents attached to an application."""
    __tablename__ = 'application_documents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    application_id = db.Column(db.String(36), db.ForeignKey('applications.id', ondelete='CASCADE'), nullable=False, index=True)
    document_type = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serialize document metadata to dictionary."""
        return {
            'id': self.id,
            'application_id': self.application_id,
            'document_type': self.document_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class Bookmark(db.Model):
    """Saved scholarships bookmarked by a student (mapped to existing 'bookmarks' table)."""
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'scholarship_id', name='unique_bookmark'),
    )

    scholarship = db.relationship('Scholarship')
    user = db.relationship('User', backref=db.backref('bookmarks', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self) -> dict:
        """Serialize bookmark to scholarship dictionary."""
        if self.scholarship:
            sch_dict = self.scholarship.to_dict()
            sch_dict['bookmarked_at'] = self.created_at.isoformat() if self.created_at else None
            return sch_dict
        return {
            'id': self.id,
            'user_id': self.user_id,
            'scholarship_id': self.scholarship_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Alias for SavedScholarship requirement
SavedScholarship = Bookmark

