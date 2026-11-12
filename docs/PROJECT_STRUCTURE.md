# Student Saarthi - Target Architecture & Project Structure

**Version:** 2.0.0 (Modular Architecture)  
**Status:** Production-Ready  
**Framework:** Flask (Application Factory Pattern) + SQLAlchemy  

---

## 1. Architecture Overview

Student Saarthi has been restructured from a monolithic prototype into a decoupled, modular, enterprise-grade web application following the **Flask Application Factory Pattern**, **Clean Architecture Principles**, and strict separation of concerns across route controllers, business logic services, data models, and presentation layouts.

```
+-----------------------------------------------------------------------+
|                           CLIENT TIER                                 |
|   HTML5 + CSS Custom Properties (Dark/Light) + Vanilla JS Components  |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                          CONTROLLER TIER                              |
|   Flask Blueprints (main, auth, student, scholarship, admin, contact) |
|   Route Decorators (@login_required, @admin_required)                 |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                            SERVICE TIER                               |
|   AuthService | ScholarshipService | ApplicationService | NotifService |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                           PERSISTENCE TIER                            |
|   SQLAlchemy 2.0 ORM Models + Migrations / Database Pool              |
|   SQLite (Default in instance/) | MySQL / PostgreSQL via DATABASE_URL |
+-----------------------------------------------------------------------+
```

---

## 2. Comprehensive Directory Structure

```
student-saarthi/
│
├── app/                                # Core Flask Application Package
│   ├── __init__.py                     # Application Factory (create_app), extension initialization
│   ├── config.py                       # Centralized configuration (Dev, Test, Prod)
│   │
│   ├── routes/                         # Modular Blueprint HTTP Route Handlers
│   │   ├── __init__.py                 # Route exports
│   │   ├── main_routes.py              # Public landing, about, contact, health, stats
│   │   ├── auth_routes.py              # Login, registration, logout, session verification
│   │   ├── scholarship_routes.py       # Scholarship directory, search, multi-filter API
│   │   ├── application_routes.py       # Application submissions, document uploads
│   │   ├── student_routes.py           # Student profile, bookmarks, notifications
│   │   ├── admin_routes.py             # Admin analytics, CRUD scholarships, user management
│   │   └── contact_routes.py           # Public inquiry message processing
│   │
│   ├── models/                         # SQLAlchemy 2.0 Data Models
│   │   ├── __init__.py                 # Model registry exports
│   │   ├── user.py                     # User (student) and Admin models + password hashing
│   │   ├── scholarship.py              # Scholarship model with verification & criteria
│   │   ├── application.py              # Application, ApplicationDocument, and Bookmark models
│   │   └── notification.py             # In-app notifications and ContactMessage models
│   │
│   ├── services/                       # Business Logic Layer (Separated from Route Handlers)
│   │   ├── __init__.py                 # Service exports
│   │   ├── auth_service.py             # Credential verification, session generation, profile updates
│   │   ├── scholarship_service.py      # Filtering, search algorithms, stats calculations
│   │   ├── application_service.py      # Validation, status workflow, file attachments, bookmarks
│   │   └── notification_service.py     # Notification creation, user alert dispatch, contact handling
│   │
│   ├── utils/                          # Reusable Utilities, Security & Validation Helpers
│   │   ├── __init__.py                 # Utility exports
│   │   ├── decorators.py               # @login_required, @admin_required authentication guards
│   │   ├── validators.py               # Email, phone, password, percentage, and file validators
│   │   └── helpers.py                  # Currency formatters, profile completion, secure uploads
│   │
│   └── templates/                      # Jinja2 Presentation Templates
│       ├── layouts/
│       │   └── base.html               # Master layout with theme switcher & mobile navbar
│       ├── partials/
│       │   ├── navbar.html             # Common navigation bar with async session detection
│       │   └── footer.html             # Common footer with links and social channels
│       ├── pages/
│       │   ├── index.html              # Landing page (hero, live stats, featured scholarships)
│       │   ├── about.html              # Mission, team, vision
│       │   ├── scholarships.html       # Scholarship directory with real-time filters
│       │   ├── scholarship_detail.html # Dedicated detail view for single scholarships
│       │   ├── apply.html              # Multi-section application form with file upload
│       │   ├── my_applications.html    # Student application tracking table with status badges
│       │   ├── student_dashboard.html  # Student dashboard (stats, recommendations, bookmarks)
│       │   ├── admin_dashboard.html    # Admin management panel (stats, table, status updates)
│       │   ├── login.html              # Student and admin unified login with Google sign-in
│       │   ├── signup.html             # Multi-step student registration form
│       │   ├── contact.html            # Contact inquiry form and office details
│       │   ├── help.html               # FAQ knowledge base
│       │   ├── privacy.html            # Privacy policy
│       │   └── terms.html              # Terms of service
│       └── errors/
│           ├── 404.html                # Resource not found error template
│           ├── 403.html                # Access forbidden template
│           └── 500.html                # Server error template
│
├── static/                             # Static Frontend Assets
│   ├── css/
│   │   └── styles.css                  # Modern responsive design system with CSS custom properties
│   ├── js/
│   │   ├── index.js                    # Landing page stats counter animations & featured cards
│   │   ├── scholarships.js             # Directory multi-filtering, search, and detail modal
│   │   ├── apply.js                    # Profile eligibility verification & application submission
│   │   ├── my_applications.js          # Student application list and status updates
│   │   ├── student_dashboard.js        # Student metrics, recommendations, and bookmarks
│   │   ├── admin_dashboard.js          # Admin controls, status update dropdowns, add modal
│   │   ├── login.js                    # Student / Admin tabbed login & Google sign-in handling
│   │   └── signup.js                   # Client-side input validation & account registration
│   ├── images/                         # Static images and banners
│   ├── icons/                          # Favicons and SVG iconography
│   └── documents/
│       └── uploads/                    # Uploaded student verification documents (ignored by Git)
│
├── instance/                           # Instance-specific Local Data (Ignored by Git)
│   └── database/
│       └── student_saarthi.db          # Default SQLite database for instant local operation
│
├── tests/                              # Automated Test Suite (Pytest)
│   ├── __init__.py                     # Test suite package
│   ├── conftest.py                     # Pytest fixtures (in-memory SQLite app, test clients)
│   ├── test_auth.py                    # Tests for registration, login, logout, validation
│   ├── test_scholarships.py            # Tests for scholarship listing, details, filtering
│   ├── test_applications.py            # Tests for application submission, duplicate prevention
│   ├── test_admin.py                   # Tests for admin authorization, CRUD, status updates
│   ├── test_routes.py                  # Tests for HTTP route rendering and static asset serving
│   └── manual/
│       └── test_endpoints.html         # Browser-based manual testing utility
│
├── scripts/                            # Operational Scripts & Database Management
│   ├── init_db.py                      # Initializes tables and triggers initial database seed
│   └── seed_db.py                      # Seeds default admin and 10 authentic scholarship programs
│
├── docs/                               # System Documentation & Audits
│   ├── PROJECT_AUDIT.md                # Comprehensive audit of existing prototype
│   ├── PROJECT_STRUCTURE.md            # Target architecture and component specification
│   ├── DATABASE_SCHEMA.md              # Entity-Relationship diagram and schema dictionary
│   ├── API_DOCUMENTATION.md            # Complete REST API reference and payload schemas
│   └── legacy_drafts/                  # Safely archived text drafts from earlier prototype
│
├── logs/                               # Application Logs
│   └── app.log                         # Rotating file log (max 1MB, 5 backups)
│
├── .venv/                              # Single Consolidated Python 3.13 Virtual Environment
├── .env                                # Local environment secrets and configuration
├── .env.example                        # Template for environment configuration
├── .gitignore                          # Comprehensive Git ignore rules
├── requirements.txt                    # Python dependency manifest
├── run.py                              # Primary application execution entry point
├── app.py                              # Backward-compatible launcher delegating to run.py
└── README.md                           # Master project guide and setup instructions
```

---

## 3. Key Architectural Decisions

1. **Application Factory (`create_app`)**:
   Enables multiple application instances with isolated configurations (such as production vs in-memory testing).
2. **Decoupled Database Access**:
   Supports both **SQLite** (`instance/database/student_saarthi.db`) for immediate zero-setup execution, and **MySQL/PostgreSQL** for enterprise production via `DATABASE_URL`.
3. **Security Enhancements**:
   - Upgraded password hashing from raw unsalted SHA256 to PBKDF2/scrypt (`werkzeug.security`).
   - Dynamic password hash migration: legacy SHA256 hashes are verified and automatically upgraded on first login.
   - Persistent `SECRET_KEY` configured via `.env` to prevent session invalidation on restart.
   - Restricted file uploads with size caps (16MB) and extension whitelisting.
4. **Dynamic API Configuration**:
   Client-side scripts use `window.location.origin + '/api'` rather than hardcoded `http://127.0.0.1:5000/api`, ensuring portability across localhost, local network IPs, and custom domains.

