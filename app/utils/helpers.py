import os
import uuid
from datetime import datetime, date
from werkzeug.utils import secure_filename

def calculate_days_left(deadline_date) -> int:
    """Calculate days remaining until scholarship deadline."""
    if not deadline_date:
        return 0
    if isinstance(deadline_date, str):
        try:
            deadline_date = datetime.strptime(deadline_date, '%Y-%m-%d').date()
        except ValueError:
            return 0
    elif isinstance(deadline_date, datetime):
        deadline_date = deadline_date.date()
        
    delta = (deadline_date - date.today()).days
    return delta

def format_currency(amount: float) -> str:
    """Format numeric amount into INR currency representation."""
    if amount is None:
        return "₹0"
    try:
        val = float(amount)
        return f"₹{val:,.2f}".rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return f"₹{amount}"

def calculate_profile_completion(user) -> int:
    """Calculate profile completion percentage based on filled attributes."""
    if not user:
        return 0
        
    tracked_fields = [
        'full_name', 'email', 'phone', 'dob', 'gender', 'address',
        'education_level', 'academic_percentage', 'field_of_study',
        'institution_name', 'graduation_year', 'category', 'annual_income'
    ]
    
    filled = 0
    for field in tracked_fields:
        val = getattr(user, field, None)
        if val is not None and str(val).strip() != '':
            filled += 1
            
    pct = int((filled / len(tracked_fields)) * 100)
    return max(pct, 40) # Minimum baseline

def save_uploaded_file(file_storage, target_directory: str, subfolder: str = None) -> tuple[str, str, int]:
    """
    Safely save an uploaded file with a UUID-prefixed secure name.
    Returns: (stored_file_name, full_file_path, file_size_in_bytes)
    """
    original_name = secure_filename(file_storage.filename)
    unique_prefix = uuid.uuid4().hex[:12]
    unique_filename = f"{unique_prefix}_{original_name}"
    
    dest_dir = os.path.join(target_directory, subfolder) if subfolder else target_directory
    os.makedirs(dest_dir, exist_ok=True)
    
    full_path = os.path.join(dest_dir, unique_filename)
    file_storage.save(full_path)
    file_size = os.path.getsize(full_path)
    
    rel_path = os.path.join(subfolder, unique_filename) if subfolder else unique_filename
    return unique_filename, rel_path.replace('\\', '/'), file_size

