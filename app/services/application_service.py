import uuid
from datetime import datetime
from app import db
from app.models.application import Application, ApplicationDocument, Bookmark
from app.models.scholarship import Scholarship
from app.models.notification import Notification

VALID_STATUSES = [
    'Draft',
    'Submitted',
    'Under Review',
    'Additional Information Required',
    'Approved',
    'Rejected'
]

class ApplicationService:
    """Service handling scholarship applications, reviews, and bookmarks."""

    @staticmethod
    def apply(user_id: str, scholarship_id: int, statement_of_purpose: str,
              achievements: str = '', extracurricular: str = '', additional_info: str = '',
              documents: list[dict] = None) -> tuple[bool, dict, str]:
        """Submit a scholarship application."""
        # Verify scholarship exists and is active
        scholarship = db.session.get(Scholarship, scholarship_id)
        if not scholarship:
            return False, {}, "Scholarship not found"

        if scholarship.status != 'active':
            return False, {}, "This scholarship is no longer accepting applications"

        # Check for existing application
        existing = Application.query.filter_by(user_id=user_id, scholarship_id=scholarship_id).first()
        if existing:
            return False, {}, "You have already applied to this scholarship"

        app_id = str(uuid.uuid4())
        application = Application(
            id=app_id,
            user_id=user_id,
            scholarship_id=scholarship_id,
            application_status='Submitted',
            statement_of_purpose=statement_of_purpose,
            academic_achievements=achievements,
            extracurricular_activities=extracurricular,
            additional_info=additional_info
        )

        # Attach documents if provided
        if documents:
            for doc in documents:
                doc_record = ApplicationDocument(
                    application_id=app_id,
                    document_type=doc.get('document_type', 'Supporting Document'),
                    file_name=doc['file_name'],
                    file_path=doc['file_path'],
                    file_size=doc.get('file_size')
                )
                db.session.add(doc_record)

        # Increment current applicants count
        scholarship.current_applicants = (scholarship.current_applicants or 0) + 1

        # Create user notification
        notif = Notification(
            user_id=user_id,
            title="Application Submitted",
            message=f"Your application for '{scholarship.name}' has been successfully submitted.",
            notification_type="success",
            link="/my-application.html"
        )
        db.session.add(notif)

        try:
            db.session.add(application)
            db.session.commit()
            return True, application.to_dict(), "Application submitted successfully"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Error submitting application: {str(e)}"

    @staticmethod
    def get_student_applications(user_id: str) -> list[dict]:
        """Fetch all applications for a student ordered by applied date."""
        applications = (Application.query
                        .filter_by(user_id=user_id)
                        .order_by(Application.applied_date.desc())
                        .all())
        return [app.to_dict() for app in applications]

    @staticmethod
    def get_all_applications(status: str = None) -> list[dict]:
        """Fetch applications across all students for admin dashboard."""
        query = Application.query
        if status:
            query = query.filter_by(application_status=status)
        applications = query.order_by(Application.applied_date.desc()).all()
        return [app.to_dict() for app in applications]

    @staticmethod
    def update_status(application_id: str, new_status: str, admin_notes: str = None) -> tuple[bool, dict, str]:
        """Update status and notes on an application."""
        if new_status not in VALID_STATUSES:
            return False, {}, f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"

        application = db.session.get(Application, application_id)
        if not application:
            return False, {}, "Application not found"

        old_status = application.application_status
        application.application_status = new_status
        if admin_notes is not None:
            application.admin_notes = admin_notes
        application.last_updated = datetime.utcnow()

        # Notify student of status update
        notif = Notification(
            user_id=application.user_id,
            title=f"Application {new_status}",
            message=f"Your application for '{application.scholarship.name if application.scholarship else 'Scholarship'}' status was updated to '{new_status}'.",
            notification_type="info" if new_status != 'Approved' else "success",
            link="/my-application.html"
        )
        db.session.add(notif)

        try:
            db.session.commit()
            return True, application.to_dict(), "Application status updated successfully"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Error updating application status: {str(e)}"

    @staticmethod
    def add_bookmark(user_id: str, scholarship_id: int) -> tuple[bool, str]:
        """Save a scholarship to student bookmarks."""
        existing = Bookmark.query.filter_by(user_id=user_id, scholarship_id=scholarship_id).first()
        if existing:
            return False, "Scholarship already bookmarked"

        scholarship = db.session.get(Scholarship, scholarship_id)
        if not scholarship:
            return False, "Scholarship not found"

        bookmark = Bookmark(user_id=user_id, scholarship_id=scholarship_id)
        try:
            db.session.add(bookmark)
            db.session.commit()
            return True, "Scholarship bookmarked successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to add bookmark: {str(e)}"

    @staticmethod
    def remove_bookmark(user_id: str, scholarship_id: int) -> tuple[bool, str]:
        """Remove a scholarship from bookmarks."""
        bookmark = Bookmark.query.filter_by(user_id=user_id, scholarship_id=scholarship_id).first()
        if not bookmark:
            return False, "Bookmark not found"

        try:
            db.session.delete(bookmark)
            db.session.commit()
            return True, "Bookmark removed successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to remove bookmark: {str(e)}"

    @staticmethod
    def get_student_bookmarks(user_id: str) -> list[dict]:
        """Get all bookmarks for a student."""
        bookmarks = (Bookmark.query
                     .filter_by(user_id=user_id)
                     .order_by(Bookmark.created_at.desc())
                     .all())
        return [b.to_dict() for b in bookmarks if b.scholarship is not None]
