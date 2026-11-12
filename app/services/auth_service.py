import uuid
from datetime import datetime
from app import db
from app.models.user import User, Admin
from app.utils.helpers import calculate_profile_completion

class AuthService:
    """Service handling user/admin authentication and profile lifecycle."""

    @staticmethod
    def register_user(data: dict) -> tuple[bool, dict, str]:
        """Register a new student account."""
        email = data.get('email', '').strip().lower()
        
        # Check duplicate
        existing = User.query.filter_by(email=email).first()
        if existing:
            return False, {}, "Email already registered"

        # Parse date of birth if provided
        dob_val = None
        if data.get('dob'):
            try:
                dob_val = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                dob_val = None

        user = User(
            id=str(uuid.uuid4()),
            full_name=data.get('fullName', '').strip(),
            email=email,
            phone=data.get('phone', '').strip(),
            dob=dob_val,
            gender=data.get('gender'),
            address=data.get('address'),
            education_level=data.get('educationLevel'),
            academic_percentage=float(data['academicPercentage']) if data.get('academicPercentage') is not None else None,
            field_of_study=data.get('fieldOfStudy'),
            institution_name=data.get('institutionName'),
            graduation_year=int(data['graduationYear']) if data.get('graduationYear') else None,
            category=data.get('category'),
            annual_income=int(data['annualIncome']) if data.get('annualIncome') else None,
            special_circumstances=data.get('specialCircumstances'),
            role='student'
        )
        user.set_password(data['password'])
        user.profile_completion = calculate_profile_completion(user)

        try:
            db.session.add(user)
            db.session.commit()
            return True, user.to_dict(), "Registration successful"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Database error during registration: {str(e)}"

    @staticmethod
    def login_user(email: str, raw_password: str) -> tuple[bool, dict, str]:
        """Authenticate student by email and password."""
        if not email or not raw_password:
            return False, {}, "Email and password are required"

        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user or not user.check_password(raw_password):
            return False, {}, "Invalid email or password"

        return True, user.to_dict(), "Login successful"

    @staticmethod
    def login_admin(username: str, raw_password: str) -> tuple[bool, dict, str]:
        """Authenticate administrator by username and password."""
        if not username or not raw_password:
            return False, {}, "Username and password are required"

        admin = Admin.query.filter_by(username=username.strip()).first()
        if not admin or not admin.check_password(raw_password):
            return False, {}, "Invalid admin credentials"

        return True, admin.to_dict(), "Admin login successful"

    @staticmethod
    def google_auth(google_user: dict) -> tuple[bool, dict, str]:
        """Authenticate or register student via Google OAuth credentials."""
        email = google_user.get('email', '').strip().lower()
        if not email:
            return False, {}, "Email required for Google authentication"

        user = User.query.filter_by(email=email).first()
        if user:
            return True, user.to_dict(), "Login successful"

        # Create new user for first-time Google sign in
        user = User(
            id=str(uuid.uuid4()),
            full_name=google_user.get('name', 'Google User'),
            email=email,
            profile_completion=45,
            role='student'
        )
        # Assign secure random password
        user.set_password(str(uuid.uuid4()))

        try:
            db.session.add(user)
            db.session.commit()
            return True, user.to_dict(), "Account created and logged in successfully"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Google authentication failed: {str(e)}"

    @staticmethod
    def get_user_profile(user_id: str) -> dict | None:
        """Fetch user profile without sensitive password data."""
        user = db.session.get(User, user_id)
        return user.to_dict() if user else None

    @staticmethod
    def update_user_profile(user_id: str, updates: dict) -> tuple[bool, dict, str]:
        """Update student profile details and recompute completion metric."""
        user = db.session.get(User, user_id)
        if not user:
            return False, {}, "User not found"

        allowed_fields = [
            'full_name', 'phone', 'address', 'education_level',
            'academic_percentage', 'field_of_study', 'institution_name',
            'graduation_year', 'category', 'annual_income', 'special_circumstances'
        ]

        for field in allowed_fields:
            if field in updates:
                setattr(user, field, updates[field])

        user.profile_completion = calculate_profile_completion(user)
        user.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return True, user.to_dict(), "Profile updated successfully"
        except Exception as e:
            db.session.rollback()
            return False, {}, f"Profile update error: {str(e)}"
