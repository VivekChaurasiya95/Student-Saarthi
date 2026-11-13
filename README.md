# Student Saarthi - All-in-One Scholarship Portal

[![Live Demo](https://img.shields.io/badge/Live_Demo-student--saarthi.antideploy.app-blue?style=for-the-badge&logo=google-chrome)](https://student-saarthi.antideploy.app)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-28%20Passed-brightgreen.svg)]()

**Student Saarthi** is an enterprise-grade, full-stack scholarship discovery, matching, and application portal. It bridges the gap between deserving students across India and central, state, and private scholarship foundations by simplifying discovery, eligibility checks, document management, and application lifecycle tracking.

🌐 **Live Production URL:** [https://student-saarthi.antideploy.app](https://student-saarthi.antideploy.app)

---

## 🌟 Key Features

### 🎓 For Students
- **Smart Eligibility Matching:** Filter scholarships by category (Academic & Merit, Central Govt Schemes, SC/ST, OBC, Minority, Girl Students, PwD, Research & Fellowship), education level, minimum cutoffs, financial benefits, and upcoming deadlines.
- **100% Verified Schemes:** Authoritative records with direct links to verified official portals (National Scholarship Portal `scholarships.gov.in`, UGC, DST INSPIRE, and corporate CSR initiatives).
- **Simple Application Workflow:** Reusable profile with Statement of Purpose, academic details, and multi-file document uploads (PDF, PNG, JPG).
- **Personalized Student Dashboard:** Real-time metrics for eligible scholarships, saved bookmarks, active application tracking, and automated status alerts.
- **Theme-Adaptive Experience:** Seamless light and dark theme modes with zero-flicker transitions.

### 🛡️ For Administrators
- **Executive Analytics:** Overview of registered students, published schemes, submitted applications, and review workloads.
- **Application Review:** Inspect complete student submissions, evaluate statements of purpose, view uploaded verification documents, and transition states (`Submitted` → `Under Review` → `Approved` / `Rejected`) with administrative feedback.
- **Scholarship Management:** Create, edit, verify, and archive scholarship programs directly from the dashboard.
- **Student Directory:** Inspect student profiles, qualification cutoffs, and demographic distribution.

---

## 👥 The Team

| Name | Role | Responsibilities |
| :--- | :--- | :--- |
| **Vivek Chaurasiya** | Founder & Lead Architect | System architecture, full-stack development, and deployment engineering |
| **Prajwal Patidar** | Database Management & Architecture | Relational schemas, query optimization, indexing, and data security |
| **Atul Dehariya** | Scholarship Research & Operations | Catalog research, eligibility criteria verification, and scheme validation |

---

## 🏗️ Architecture & Technology Stack

- **Backend:** Python 3.13, Flask 3.0.0 utilizing the **Application Factory Pattern** (`create_app`) and modular **Blueprints**.
- **ORM / Database:** **SQLAlchemy 2.0** with SQLite default (`instance/database/student_saarthi.db`) and drop-in support for PostgreSQL and MySQL via `DATABASE_URL`.
- **Frontend:** Jinja2 templating with modular layouts (`app/templates/layouts/base.html`), reusable partials (`navbar.html`, `footer.html`), semantic CSS3 design tokens, and modular vanilla JavaScript.
- **Security:**
  - Password hashing via secure cryptographic hashing.
  - Role-based route decorators (`@login_required`, `@admin_required`).
  - Whitelist-based file upload validation with sanitized storage.
  - SQL injection protection via parameterized ORM queries.
  - Session verification singleton to prevent duplicate client API calls.

---

## 📁 Project Directory Structure

```
Student Saarthi/
├── app/                           # Core Flask Application Package
│   ├── __init__.py                # Application Factory (create_app) & SQLAlchemy init
│   ├── config.py                  # Environment configurations (Dev, Test, Prod)
│   ├── models/                    # SQLAlchemy 2.0 ORM Data Models
│   │   ├── user.py                # User (Student) and Admin entities
│   │   ├── scholarship.py         # Scholarship opportunity model
│   │   ├── application.py         # Application, ApplicationDocument, Bookmark
│   │   └── notification.py        # Notification and ContactMessage models
│   ├── routes/                    # Modular Flask Blueprints
│   │   ├── main_routes.py         # Public portal pages (Home, About, Help, etc.)
│   │   ├── auth_routes.py         # Authentication (Register, Login, Admin Login, Session)
│   │   ├── scholarship_routes.py  # Scholarship browsing, search, and detail API
│   │   ├── application_routes.py  # Student application workflow and submissions
│   │   ├── student_routes.py      # Student profile, bookmarks, notifications API
│   │   ├── admin_routes.py        # Admin dashboard, application review, CRUD API
│   │   └── contact_routes.py      # Public contact inquiries
│   ├── services/                  # Business Logic Layer
│   │   ├── auth_service.py        # Authentication & profile management
│   │   ├── scholarship_service.py # Scholarship catalog and filter queries
│   │   ├── application_service.py # Application lifecycle and file handling
│   │   └── notification_service.py# Alerts and contact inquiry processing
│   ├── utils/                     # Helper Utilities & Security
│   │   ├── decorators.py          # @login_required, @admin_required
│   │   ├── validators.py          # Input and file extension validators
│   │   └── helpers.py             # File saving and slug generation
│   └── templates/                 # Jinja2 Templates
│       ├── layouts/               # base.html layout template
│       ├── partials/              # navbar.html, footer.html
│       ├── pages/                 # Full responsive application pages
│       └── errors/                # 404.html, 403.html, 500.html
├── docs/                          # Technical Documentation
│   ├── DATABASE_SCHEMA.md         # Schema specs, ER diagram, relationships
│   ├── API_DOCUMENTATION.md       # Complete RESTful API specifications
│   ├── PROJECT_STRUCTURE.md       # Module responsibilities and architecture
│   └── PROJECT_AUDIT.md           # Architecture audit log
├── scripts/                       # Database & Deployment Utilities
│   ├── init_db.py                 # Automated schema table creator
│   ├── seed_db.py                 # Seeds default admin and 10 verified scholarships
│   └── antideploy_client.py       # Cloud deployment client
├── static/                        # Frontend Static Assets
│   ├── css/styles.css             # Theme-adaptive stylesheet
│   └── js/                        # Modular client-side JavaScript controllers
├── tests/                         # Pytest Automated Test Suite (28 Tests)
├── .env.example                   # Environment variable template
├── .gitignore                     # Comprehensive git exclusion rules
├── LICENSE                        # MIT License
├── Procfile                       # Production process declaration
├── requirements.txt               # Pinned Python package dependencies
├── run.py                         # Primary application entrypoint
└── README.md                      # Project documentation and setup guide
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Python:** 3.10+ (Recommended: Python 3.12 or 3.13)
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/VivekChaurasiya95/Student-Saarthi.git
cd Student-Saarthi
```

### 3. Create & Activate Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

### 6. Initialize & Seed Database
```bash
python scripts/init_db.py
python scripts/seed_db.py
```

### 7. Run the Application
```bash
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Default Administrator Credentials

To access the Admin Dashboard at `http://127.0.0.1:5000/login.html` (toggle **Admin Portal**):

- **Admin Username:** `admin`
- **Admin Password:** `admin123`
- **Role:** Administrator (Full administrative access)

---

## 🧪 Running Automated Tests

The application includes an automated test suite with **26 unit and integration tests** covering authentication, role-based access, scholarship filtering, document uploads, application state updates, and routing.

```bash
pytest tests -v
```

Output:
```
============================= 26 passed in 4.50s =============================
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2026 Vivek Chaurasiya, Prajwal Patidar, Atul Dehariya
```
