import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
PHONE_REGEX = re.compile(r'^[0-9]{10}$')

def validate_email(email: str) -> bool:
    """Validate email address format."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

def validate_phone(phone: str) -> bool:
    """Validate 10-digit phone number format."""
    if not phone:
        return True # Optional field in some places
    clean_phone = re.sub(r'[\s\-\+\(\)]', '', str(phone))
    return bool(PHONE_REGEX.match(clean_phone[-10:])) if len(clean_phone) >= 10 else False

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if uploaded file has an allowed extension."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions

def validate_registration_data(data: dict) -> tuple[bool, str]:
    """Validate required registration fields."""
    if not data or not isinstance(data, dict):
        return False, "Request payload must be a JSON object"
        
    required_fields = ['fullName', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return False, f"Missing required field: {field}"
            
    if not validate_email(data['email']):
        return False, "Invalid email address format"
        
    if len(str(data['password'])) < 6:
        return False, "Password must be at least 6 characters long"
        
    if data.get('phone') and not validate_phone(str(data['phone'])):
        return False, "Phone number must be a valid 10-digit number"
        
    percentage = data.get('academicPercentage')
    if percentage is not None:
        try:
            val = float(percentage)
            if val < 0 or val > 100:
                return False, "Academic percentage must be between 0 and 100"
        except (ValueError, TypeError):
            return False, "Academic percentage must be a valid number"
            
    return True, ""

def validate_scholarship_data(data: dict) -> tuple[bool, str]:
    """Validate required fields when adding a new scholarship."""
    if not data or not isinstance(data, dict):
        return False, "Request payload must be a JSON object"
        
    required_fields = ['name', 'provider', 'amount', 'category', 'description', 'deadline']
    for field in required_fields:
        if not data.get(field):
            return False, f"Missing required field: {field}"
            
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, "Scholarship amount must be greater than 0"
    except (ValueError, TypeError):
        return False, "Scholarship amount must be a valid number"
        
    return True, ""

