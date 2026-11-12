# Student Saarthi - All-in-One Scholarship Portal

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/Tests-26%20Passed-brightgreen.svg)]()

**Student Saarthi** is an enterprise-grade, full-stack scholarship discovery, matching, and application portal. It bridges the gap between deserving students and national/private scholarship providers by simplifying discovery, eligibility verification, document management, and application lifecycle tracking.

---

## 🌟 Key Features

### 🎓 For Students
- **Intelligent Discovery & Filtering:** Search and filter scholarships by category (Merit, Need-based, Minority, STEM), education level, minimum academic cutoffs, financial benefits, and upcoming deadlines.
- **Accurate Information:** Authoritative records with direct links to verified official portals (e.g. National Scholarship Portal, UGC, INSPIRE, state departments) with complete transparency.
- **Seamless Application Process:** Apply directly through the portal with statement of purpose, academic honors, extracurriculars, and multi-file document uploads (PDF, PNG, JPG).
- **Personalized Student Dashboard:** Real-time metrics for eligible scholarships, saved bookmarks, active applications, real-time application status tracking, and notification alerts.
- **Profile Management:** Dynamic profile completion calculation (0–100%) tracking academic and socioeconomic details.

### 🛡️ For Administrators
- **Executive Analytics:** Overview of registered students, published scholarships, submitted applications, and pending review counts.
- **Application Review:** Inspect complete student applications, evaluate statements of purpose, view uploaded verification documents, and transition states (`Submitted` → `Under Review` → `Approved` / `Rejected`) with administrative notes.
- **Scholarship Management:** Create, edit, verify, and delete scholarship opportunities directly from the dashboard.
- **Student Directory:** View student profiles and demographic distributions.

### 🌐 Public Portal & Compliance
- Fully responsive, accessible, mobile-first design preserving original visual identity.
- Dedicated pages for About Us, Help Center & FAQ, Contact Inquiries, Terms of Service, and Privacy Policy.

---

## 🏗️ Architecture & Technology Stack

- **Backend:** Python 3.13, Flask 3.0.0 utilizing the **Application Factory Pattern** (`create_app`) and modular **Blueprints**.
- **ORM / Database:** **SQLAlchemy 2.0** with SQLite default (`instance/database/student_saarthi.db`) and drop-in support for MySQL and PostgreSQL via `DATABASE_URL`.
- **Frontend:** Jinja2 templating with reusable base layouts (`app/templates/layouts/base.html`), partials (`navbar.html`, `footer.html`), semantic CSS3, and dynamic vanilla JavaScript.
- **Security:**
  - Password hashing via PBKDF2/scrypt (with transparent upgrade path from legacy SHA256).
  - Secure session management with role-based route decorators (`@login_required`, `@admin_required`).
  - Whitelist-based file upload validation with sanitized path storage.
  - SQL injection protection via parameterized ORM queries.

---

## 📁 Project Directory Structure

```
D:\Student Saarthi\
├── app/                           # Core Flask Application Package
│   ├── __init__.py                # Application Factory (create_app) & SQLAlchemy init
│   ├── config.py                  # Environment configurations (Dev, Test, Prod)
│   ├── models/                    # SQLAlchemy 2.0 ORM Data Models
│   │   ├── __init__.py
│   │   ├── user.py                # User (Student) and Admin entities
│   │   ├── scholarship.py         # Scholarship opportunity model
│   │   ├── application.py         # Application, ApplicationDocument, Bookmark
│   │   └── notification.py        # Notification and ContactMessage models
│   ├── routes/                    # Modular Flask Blueprints
│   │   ├── __init__.py
│   │   ├── main_routes.py         # Public portal pages (Home, About, Help, etc.)
│   │   ├── auth_routes.py         # Authentication (Register, Login, Admin Login, Session)
│   │   ├── scholarship_routes.py  # Scholarship browsing, search, and detail API
│   │   ├── application_routes.py  # Student application workflow and submissions
│   │   ├── student_routes.py      # Student profile, bookmarks, notifications API
│   │   ├── admin_routes.py        # Admin dashboard, application review, CRUD API
│   │   └── contact_routes.py      # Public contact inquiries
│   ├── services/                  # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication & profile management
│   │   ├── scholarship_service.py # Scholarship catalog and filter queries
│   │   ├── application_service.py # Application lifecycle and file handling
│   │   └── notification_service.py# Alerts and contact inquiry processing
│   ├── utils/                     # Helper Utilities & Security
│   │   ├── __init__.py
│   │   ├── decorators.py          # @login_required, @admin_required
│   │   ├── validators.py          # Input and file extension validators
│   │   └── helpers.py             # File saving and slug generation
│   └── templates/                 # Jinja2 Templates
│       ├── layouts/               # base.html layout template
│       ├── partials/              # navbar.html, footer.html
│       ├── pages/                 # Full responsive application pages
│       └── errors/                # 404.html, 403.html, 500.html
├── docs/                          # Comprehensive Technical Documentation
│   ├── PROJECT_AUDIT.md           # Exhaustive initial audit and refactoring log
│   ├── PROJECT_STRUCTURE.md       # Directory layout and module responsibilities
│   ├── DATABASE_SCHEMA.md         # Schema specs, ER diagram, relationships
│   ├── API_DOCUMENTATION.md       # Complete RESTful API specifications
│   └── legacy_drafts/             # Safely archived legacy prototype files
├── instance/
│   └── database/                  # SQLite database location (student_saarthi.db)
├── scripts/                       # Database Management Scripts
│   ├── init_db.py                 # Automated schema table creator
│   └── seed_db.py                 # Seeds default admin and 10 verified scholarships
├── static/                        # Frontend Static Assets
│   ├── css/styles.css             # Main stylesheet
│   ├── js/                        # Modular client-side JavaScript controllers
│   ├── images/                    # UI branding, logos, and banners
│   ├── icons/                     # SVG icons
│   └── documents/                 # Uploaded application verification files
├── tests/                         # Pytest Automated Test Suite (26 Tests)
│   ├── conftest.py                # Test fixtures, mock clients, test database
│   ├── test_auth.py               # Authentication tests (Register, Login, Admin)
│   ├── test_scholarships.py       # Catalog query, filter, and detail tests
│   ├── test_applications.py       # Application submission and document upload tests
│   ├── test_admin.py              # Admin authorization and application review tests
│   └── test_routes.py             # Public and student page routing tests
├── .env                           # Local environment configuration (git ignored)
├── .env.example                   # Environment variable template
├── .gitignore                     # Git exclusion rules
├── requirements.txt               # Pinned Python package dependencies
├── run.py                         # Primary application entrypoint
├── app.py                         # WSGI compatibility entrypoint
└── README.md                      # Project documentation and setup guide
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Python:** 3.10, 3.11, 3.12, or 3.13
- **Virtual Environment:** Use the unified `.venv` environment.

### 2. Activate Virtual Environment
On Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
*Or directly invoke the virtual environment binary:*
```powershell
.\.venv\Scripts\python.exe
```

### 3. Install Dependencies
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` (pre-configured with secure defaults for local development):
```powershell
Copy-Item .env.example .env
```

Key environment options in `.env`:
```ini
FLASK_ENV=development
SECRET_KEY=change-this-to-a-very-secret-key-in-production
DATABASE_URL=sqlite:///instance/database/student_saarthi.db
MAX_CONTENT_LENGTH=16777216
```

### 5. Initialize & Seed Database
Initialize database tables and seed verified scholarships and default admin account:
```powershell
# Create tables
.\.venv\Scripts\python.exe scripts/init_db.py

# Seed default admin and 10 real scholarships
.\.venv\Scripts\python.exe scripts/seed_db.py
```

### 6. Run the Application
Start the development server:
```powershell
.\.venv\Scripts\python.exe run.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Default Administrator Credentials

To access the Admin Dashboard at `http://127.0.0.1:5000/admin/dashboard` or `http://127.0.0.1:5000/login`:

- **Admin Username:** `admin`
- **Admin Password:** `admin123`
- **Role:** Administrator (full access to applications, scholarships, and user records)

---

## 🧪 Running Automated Tests

The application includes an automated test suite with **26 passing unit and integration tests** covering authentication, role-based access, scholarship filtering, document uploads, application state updates, and public route rendering.

Run tests using pytest:
```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

Output:
```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1
rootdir: D:\Student Saarthi
collected 26 items

tests\test_admin.py::test_admin_login_success PASSED                     [  3%]
tests\test_admin.py::test_admin_login_invalid PASSED                     [  7%]
tests\test_admin.py::test_admin_dashboard_protected PASSED               [ 11%]
tests\test_admin.py::test_admin_get_applications PASSED                  [ 15%]
tests\test_admin.py::test_admin_update_application_status PASSED         [ 19%]
tests\test_admin.py::test_admin_create_scholarship PASSED                [ 23%]
tests\test_admin.py::test_admin_delete_scholarship PASSED                [ 26%]
tests\test_applications.py::test_apply_scholarship_success PASSED        [ 30%]
tests\test_applications.py::test_apply_duplicate_prevention PASSED       [ 34%]
tests\test_applications.py::test_apply_sop_too_short PASSED              [ 38%]
tests\test_applications.py::test_apply_requires_login PASSED             [ 42%]
tests\test_applications.py::test_get_student_applications PASSED         [ 46%]
tests\test_applications.py::test_bookmark_scholarship PASSED             [ 50%]
tests\test_auth.py::test_register_user_success PASSED                    [ 53%]
tests\test_auth.py::test_register_duplicate_email PASSED                 [ 57%]
tests\test_auth.py::test_login_success PASSED                            [ 61%]
tests\test_auth.py::test_login_invalid_password PASSED                  [ 65%]
tests\test_auth.py::test_check_session PASSED                            [ 69%]
tests\test_auth.py::test_logout PASSED                                   [ 73%]
tests\test_routes.py::test_home_page PASSED                              [ 76%]
tests\test_routes.py::test_public_pages PASSED                           [ 80%]
tests\test_routes.py::test_student_dashboard_redirect_if_unauth PASSED   [ 84%]
tests\test_scholarships.py::test_get_all_scholarships PASSED             [ 88%]
tests\test_scholarships.py::test_filter_scholarships_by_category PASSED  [ 92%]
tests\test_scholarships.py::test_filter_scholarships_by_amount PASSED    [ 96%]
tests\test_scholarships.py::test_get_scholarship_detail PASSED          [100%]

============================= 26 passed in 10.12s =============================
```

---

## 📖 Technical Documentation

- 📄 [Project Audit & Refactoring Log](docs/PROJECT_AUDIT.md) - Details on legacy architecture, audit findings, and refactoring decisions.
- 📐 [Project Structure & Blueprint Architecture](docs/PROJECT_STRUCTURE.md) - Deep dive into folder architecture, module responsibilities, and routing.
- 🗄️ [Database Schema Specifications](docs/DATABASE_SCHEMA.md) - Entity-Relationship diagram, table definitions, foreign keys, and indexes.
- 🔌 [RESTful API Documentation](docs/API_DOCUMENTATION.md) - Comprehensive API documentation with request payloads, status codes, and responses.

---

## 📜 License & Compliance

Student Saarthi is developed as an educational open-access scholarship discovery portal. All scholarship information is cataloged from public, official government portals (such as National Scholarship Portal scholarships.gov.in, UGC, and DST INSPIRE) and verified private corporate social responsibility (CSR) initiatives.

