from app.models.user import User, Admin
from app.models.scholarship import Scholarship
from app.models.application import Application, ApplicationDocument, Bookmark, SavedScholarship
from app.models.notification import Notification, ContactMessage

__all__ = [
    'User',
    'Admin',
    'Scholarship',
    'Application',
    'ApplicationDocument',
    'Bookmark',
    'SavedScholarship',
    'Notification',
    'ContactMessage'
]

