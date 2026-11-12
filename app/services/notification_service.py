from app import db
from app.models.notification import Notification, ContactMessage

class NotificationService:
    """Service handling notifications and user inquiry messages."""

    @staticmethod
    def create(user_id: str, title: str, message: str, notification_type: str = 'info', link: str = None) -> Notification:
        """Create a new user notification."""
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link
        )
        try:
            db.session.add(notif)
            db.session.commit()
            return notif
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def get_user_notifications(user_id: str, unread_only: bool = False) -> list[dict]:
        """Fetch notifications for a user."""
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        notifs = query.order_by(Notification.created_at.desc()).all()
        return [n.to_dict() for n in notifs]

    @staticmethod
    def mark_read(notification_id: int, user_id: str) -> bool:
        """Mark a single notification as read."""
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            try:
                db.session.commit()
                return True
            except Exception:
                db.session.rollback()
        return False

    @staticmethod
    def mark_all_read(user_id: str) -> bool:
        """Mark all notifications as read for a user."""
        try:
            Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def save_contact(name: str, email: str, subject: str, message: str) -> tuple[bool, str]:
        """Save a message submitted through the Contact form."""
        if not name or not email or not message:
            return False, "Name, email, and message are required"

        msg = ContactMessage(
            name=name.strip(),
            email=email.strip().lower(),
            subject=subject.strip() if subject else "General Inquiry",
            message=message.strip()
        )
        try:
            db.session.add(msg)
            db.session.commit()
            return True, "Message sent successfully! Our team will get back to you soon."
        except Exception as e:
            db.session.rollback()
            return False, f"Error saving contact message: {str(e)}"

