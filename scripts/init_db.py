import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from scripts.seed_db import seed_database

def init_db():
    """Create all tables and seed default data."""
    app = create_app()
    with app.app_context():
        print("🔧 Creating database tables...")
        db.create_all()
        print("✅ Tables created.")
        seed_database()

if __name__ == '__main__':
    init_db()

