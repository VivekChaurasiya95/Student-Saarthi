from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_
from app import db
from app.models.scholarship import Scholarship
from app.models.user import User
from app.models.application import Application

class ScholarshipService:
    """Service handling scholarship discovery, filtering, and management."""

    @staticmethod
    def get_all(status: str = 'active', search: str = None, category: str = None,
                min_amount: float = None, max_amount: float = None,
                education_level: str = None, days_deadline: int = None) -> list[dict]:
        """Fetch scholarships with multi-attribute filtering."""
        query = Scholarship.query

        if status:
            query = query.filter(Scholarship.status == status)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Scholarship.name.ilike(search_pattern),
                    Scholarship.provider.ilike(search_pattern),
                    Scholarship.description.ilike(search_pattern),
                    Scholarship.category.ilike(search_pattern)
                )
            )

        if category:
            query = query.filter(Scholarship.category.ilike(f"%{category.strip()}%"))

        if min_amount is not None:
            query = query.filter(Scholarship.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Scholarship.amount <= max_amount)

        if education_level:
            query = query.filter(Scholarship.education_levels.ilike(f"%{education_level.strip()}%"))

        if days_deadline is not None and days_deadline > 0:
            target_date = date.today() + timedelta(days=days_deadline)
            query = query.filter(
                and_(
                    Scholarship.deadline >= date.today(),
                    Scholarship.deadline <= target_date
                )
            )

        query = query.order_by(Scholarship.created_at.desc())
        scholarships = query.all()
        return [s.to_dict() for s in scholarships]

    @staticmethod
    def get_featured(limit: int = 6) -> list[dict]:
        """Get latest active scholarships for landing page."""
        scholarships = (Scholarship.query
                        .filter_by(status='active')
                        .order_by(Scholarship.created_at.desc())
                        .limit(limit)
                        .all())
        return [s.to_dict() for s in scholarships]

    @staticmethod
    def get_by_id(scholarship_id: int) -> dict | None:
        """Fetch single scholarship by ID."""
        scholarship = db.session.get(Scholarship, scholarship_id)
        return scholarship.to_dict() if scholarship else None

    @staticmethod
    def create(data: dict) -> tuple[bool, dict, str]:
        """Create a new scholarship."""
        deadline_val = None
        if data.get('deadline'):
            try:
                deadline_val = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return False, {}, "Invalid deadline format. Expected YYYY-MM-DD"

        start_date_val = None
        if data.get('startDate'):
            try:
                start_date_val = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                start_date_val = None

        scholarship = Scholarship(
            name=data['name'].strip(),
            provider=data['provider'].strip(),
            amount=float(data['amount']),
            category=data['category'].strip(),
            description=data.get('description', '').strip(),
            min_percentage=float(data.get('minPercentage', 0) or 0),
            education_levels=data.get('educationLevels', ''),
            eligible_categories=data.get('eligibleCategories', ''),
            max_income=int(data['maxIncome']) if data.get('maxIncome') else None,
            age_limit=int(data['ageLimit']) if data.get('ageLimit') else None,
            start_date=start_date_val,
            deadline=deadline_val,
            application_procedure=data.get('applicationProcedure', ''),
            official_url=data.get('officialUrl', ''),
            official_source=data.get('officialSource', ''),
            is_verified=bool(data.get('isVerified', True)),
            required_documents=data.get('requiredDocuments', ''),
            status=data.get('status', 'active'),
            max_applicants=int(data['maxApplicants']) if data.get('maxApplicants') else None,
            current_applicants=0
        )

        try:
            db.session.add(scholarship)
            db.session.commit()
            return True, scholarship.to_dict(), "Scholarship added successfully"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Error adding scholarship: {str(e)}"

    @staticmethod
    def update(scholarship_id: int, data: dict) -> tuple[bool, dict, str]:
        """Update an existing scholarship."""
        scholarship = db.session.get(Scholarship, scholarship_id)
        if not scholarship:
            return False, {}, "Scholarship not found"

        fields_to_update = [
            'name', 'provider', 'category', 'description',
            'education_levels', 'eligible_categories', 'application_procedure',
            'official_url', 'official_source', 'required_documents', 'status'
        ]
        for field in fields_to_update:
            if field in data:
                setattr(scholarship, field, data[field])

        if 'amount' in data:
            scholarship.amount = float(data['amount'])
        if 'minPercentage' in data or 'min_percentage' in data:
            scholarship.min_percentage = float(data.get('minPercentage') or data.get('min_percentage', 0))
        if 'maxIncome' in data or 'max_income' in data:
            val = data.get('maxIncome') or data.get('max_income')
            scholarship.max_income = int(val) if val else None
        if 'ageLimit' in data or 'age_limit' in data:
            val = data.get('ageLimit') or data.get('age_limit')
            scholarship.age_limit = int(val) if val else None
        if 'deadline' in data and data['deadline']:
            try:
                scholarship.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                pass

        scholarship.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return True, scholarship.to_dict(), "Scholarship updated successfully"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Error updating scholarship: {str(e)}"

    @staticmethod
    def delete(scholarship_id: int) -> tuple[bool, str]:
        """Delete a scholarship by ID."""
        scholarship = db.session.get(Scholarship, scholarship_id)
        if not scholarship:
            return False, "Scholarship not found"

        try:
            db.session.delete(scholarship)
            db.session.commit()
            return True, "Scholarship deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting scholarship: {str(e)}"

    @staticmethod
    def get_stats() -> dict:
        """Calculate portal statistics."""
        active_scholarships = Scholarship.query.filter_by(status='active').count()
        total_students = User.query.filter_by(role='student').count()
        total_applications = Application.query.count()
        approved_applications = Application.query.filter_by(application_status='Approved').count()

        success_rate = round((approved_applications / total_applications * 100) if total_applications > 0 else 0.0, 1)

        return {
            'scholarships': active_scholarships,
            'students': total_students,
            'totalApplications': total_applications,
            'approvedCount': approved_applications,
            'successRate': success_rate
        }
