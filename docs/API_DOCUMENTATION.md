# Student Saarthi - RESTful API Documentation

## 1. Overview & Architecture

The **Student Saarthi** backend exposes a structured, RESTful API serving both JSON API clients and the dynamic interactive frontend.

- **Base URL:** `http://<host>:<port>` (e.g. `http://127.0.0.1:5000` or production domain)
- **Content Negotiation:**
  - JSON payloads: `Content-Type: application/json`
  - Document uploads: `Content-Type: multipart/form-data`
  - All success and failure responses return JSON objects (`application/json; charset=utf-8`)
- **Authentication & Sessions:**
  - Standard HTTP cookie sessions (`session['user_id']`, `session['admin_id']`)
  - Cross-Origin Resource Sharing (CORS) enabled with credentials support

---

## 2. Standard HTTP Response Format & Status Codes

| Code | Meaning | Usage |
| :---: | :--- | :--- |
| `200 OK` | Request Succeeded | Successful fetch, update, deletion, or query |
| `201 Created` | Resource Created | Successful registration, application submission, or scholarship creation |
| `400 Bad Request` | Validation Failure | Missing required fields, invalid email format, invalid SOP length |
| `401 Unauthorized` | Authentication Failure | Invalid credentials, expired session, or missing login |
| `403 Forbidden` | Access Denied | Student attempting to access admin endpoints |
| `404 Not Found` | Resource Not Found | Scholarship, user, or application does not exist |
| `500 Server Error` | Internal Server Error | Database failure, unhandled server exception |

Standard error payload format:
```json
{
  "error": "Descriptive message identifying validation or authorization failure"
}
```

---

## 3. Authentication & Session Endpoints

### 3.1 Register Student
Registers a new student account, hashes the password via PBKDF2/scrypt, and logs the user in.
- **Endpoint:** `POST /api/register`
- **Access:** Public
- **Request Body (JSON or Form):**
  ```json
  {
    "fullName": "Aarav Sharma",
    "email": "aarav.sharma@example.com",
    "password": "SecurePassword123",
    "phone": "+91 9876543210",
    "dob": "2004-05-15",
    "gender": "Male",
    "address": "B-42, Sector 62, Noida, UP",
    "educationLevel": "Undergraduate",
    "academicPercentage": 88.5,
    "fieldOfStudy": "Computer Science & Engineering",
    "institutionName": "National Institute of Technology",
    "graduationYear": 2026,
    "category": "General",
    "annualIncome": 350000,
    "specialCircumstances": "First generation college learner"
  }
  ```
- **Response `201 Created`:**
  ```json
  {
    "success": true,
    "userId": "d7a468d7-7fbc-49e0-82a9-b6957388cfd0",
    "message": "Registration successful"
  }
  ```

---

### 3.2 Student Login
Authenticates a student and creates an active session. Supports automatic transparent migration of legacy SHA256 passwords.
- **Endpoint:** `POST /api/login`
- **Access:** Public
- **Request Body (JSON or Form):**
  ```json
  {
    "email": "aarav.sharma@example.com",
    "password": "SecurePassword123"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "userId": "d7a468d7-7fbc-49e0-82a9-b6957388cfd0",
    "userName": "Aarav Sharma"
  }
  ```
- **Response `401 Unauthorized`:**
  ```json
  {
    "error": "Invalid email or password"
  }
  ```

---

### 3.3 Admin Login
Authenticates a portal administrator and establishes an admin session.
- **Endpoint:** `POST /api/admin/login`
- **Access:** Public
- **Request Body (JSON or Form):**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "adminId": "8f2a1b9c-4e3d-4c2a-9f1e-5b6a7c8d9e0f",
    "username": "admin"
  }
  ```

---

### 3.4 Check Session
Verifies active session status for client-side navbar and page authorization checks.
- **Endpoint:** `GET /api/check-session`
- **Access:** Public
- **Response `200 OK` (Logged In as Student):**
  ```json
  {
    "loggedIn": true,
    "userId": "d7a468d7-7fbc-49e0-82a9-b6957388cfd0",
    "userName": "Aarav Sharma",
    "type": "user"
  }
  ```
- **Response `200 OK` (Logged In as Admin):**
  ```json
  {
    "loggedIn": true,
    "adminId": "8f2a1b9c-4e3d-4c2a-9f1e-5b6a7c8d9e0f",
    "username": "admin",
    "type": "admin"
  }
  ```
- **Response `200 OK` (Guest / Not Logged In):**
  ```json
  {
    "loggedIn": false
  }
  ```

---

### 3.5 Logout
Clears current session and cookies.
- **Endpoint:** `POST /api/logout` (or `GET /api/logout`)
- **Access:** Authenticated
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "message": "Logged out successfully"
  }
  ```

---

### 3.6 Google OAuth Sign-In
Authenticates or auto-provisions a student account via Google OAuth token.
- **Endpoint:** `POST /api/auth/google`
- **Access:** Public
- **Request Body (JSON):**
  ```json
  {
    "token": "google_id_token_string",
    "email": "student@gmail.com",
    "name": "Student Name",
    "google_id": "108392817283"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "userId": "d7a468d7-7fbc-49e0-82a9-b6957388cfd0",
    "userName": "Student Name",
    "message": "Google authentication successful"
  }
  ```

---

## 4. Scholarship Discovery Endpoints

### 4.1 Browse & Filter Scholarships
Retrieves active scholarships matching optional search keywords and filter criteria.
- **Endpoint:** `GET /api/scholarships`
- **Access:** Public
- **Query Parameters:**
  - `search` (string): Search query matching scholarship name, provider, or description
  - `category` (string): Category filter (e.g. `Merit-Based`, `Need-Based`, `Government`)
  - `education` (string): Education level filter (e.g. `Undergraduate`, `Postgraduate`, `Class 12`)
  - `min_amount` (float): Minimum financial benefit
  - `max_amount` (float): Maximum financial benefit
  - `amount` (string): Amount range shorthand (e.g. `25000-50000`)
  - `deadline` (integer): Filter scholarships expiring within N days (e.g. `30`)
- **Response `200 OK`:**
  ```json
  [
    {
      "id": 1,
      "name": "Post Matric Scholarships Scheme for Minorities",
      "provider": "Ministry of Minority Affairs, Govt. of India",
      "amount": 25000.0,
      "category": "Minority / Government",
      "description": "Financial assistance for meritorious students from minority communities pursuing Class 11 to Ph.D.",
      "min_percentage": 50.0,
      "education_levels": "Class 11, Class 12, Undergraduate, Postgraduate, Ph.D.",
      "eligible_categories": "Muslim, Christian, Sikh, Buddhist, Jain, Parsi",
      "max_income": 200000,
      "age_limit": null,
      "start_date": "2026-07-01",
      "deadline": "2026-11-30",
      "application_procedure": "Apply online through the National Scholarship Portal (NSP).",
      "official_url": "https://scholarships.gov.in",
      "official_source": "National Scholarship Portal (scholarships.gov.in)",
      "is_verified": true,
      "last_verified_date": "2026-10-15",
      "required_documents": "Income Certificate, Community Certificate, Marksheets, Aadhaar Card, Bank Passbook",
      "status": "active",
      "max_applicants": 50000,
      "current_applicants": 1240,
      "created_at": "2026-11-12T10:00:00",
      "updated_at": "2026-11-12T10:00:00"
    }
  ]
  ```

---

### 4.2 Featured Scholarships
Retrieves top featured verified scholarships for the homepage hero carousel.
- **Endpoint:** `GET /api/scholarships/featured`
- **Access:** Public
- **Query Parameters:**
  - `limit` (int, default `6`): Maximum number of records to return
- **Response `200 OK`:** Array of scholarship objects.

---

### 4.3 Get Scholarship Details
Retrieves exhaustive information for a specific scholarship.
- **Endpoint:** `GET /api/scholarships/<scholarship_id>`
- **Access:** Public
- **Response `200 OK`:** Full scholarship object.
- **Response `404 Not Found`:**
  ```json
  {
    "error": "Scholarship not found"
  }
  ```

---

## 5. Application Workflow Endpoints

### 5.1 Submit Application
Submits a scholarship application with essay answers and optional document uploads.
- **Endpoint:** `POST /api/apply`
- **Access:** Authenticated Student
- **Request Format:** `multipart/form-data` or `application/json`
- **Form Data Fields:**
  - `scholarshipId` (int, required): Target scholarship ID
  - `sop` (text, required): Statement of Purpose (min 50 characters)
  - `achievements` (text, optional): Academic honors and awards
  - `extracurricular` (text, optional): Clubs, sports, volunteering
  - `additionalInfo` (text, optional): Additional context or notes
  - `documents` (file[], optional): Uploaded PDFs or images (`.pdf`, `.png`, `.jpg`, `.jpeg`, `.doc`, `.docx`)
  - `documentType` (text, optional): Label for uploaded files
- **Response `201 Created`:**
  ```json
  {
    "success": true,
    "applicationId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "message": "Application submitted successfully"
  }
  ```
- **Response `400 Bad Request`:**
  ```json
  {
    "error": "You have already applied for this scholarship"
  }
  ```

---

### 5.2 My Submitted Applications
Retrieves all applications submitted by the authenticated student along with review status and attached documents.
- **Endpoint:** `GET /api/applications`
- **Access:** Authenticated Student
- **Response `200 OK`:**
  ```json
  [
    {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "user_id": "d7a468d7-7fbc-49e0-82a9-b6957388cfd0",
      "scholarship_id": 1,
      "scholarship_name": "Post Matric Scholarships Scheme for Minorities",
      "amount": 25000.0,
      "provider": "Ministry of Minority Affairs, Govt. of India",
      "deadline": "2026-11-30",
      "application_status": "Under Review",
      "statement_of_purpose": "My career aspiration is to pursue research in Computer Science...",
      "academic_achievements": "State Rank 14 in Senior Secondary Examination",
      "extracurricular_activities": "Team lead of College Robotics Club",
      "additional_info": "First-generation learner",
      "applied_date": "2026-11-12T14:30:00",
      "last_updated": "2026-11-12T14:30:00",
      "admin_notes": "Academic documents verified; awaiting financial clearance",
      "documents": [
        {
          "id": 1,
          "application_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
          "document_type": "Income Certificate",
          "file_name": "income_cert.pdf",
          "file_path": "static/documents/applications/income_cert_20261112.pdf",
          "file_size": 245100,
          "uploaded_at": "2026-11-12T14:30:00"
        }
      ]
    }
  ]
  ```

---

## 6. Student Dashboard & Profile Endpoints

### 6.1 Get / Update Profile
- **Get Profile:** `GET /api/profile`
  - **Access:** Authenticated Student
  - **Response `200 OK`:** Full student user object.
- **Update Profile:** `PUT /api/profile`
  - **Access:** Authenticated Student
  - **Request Body (JSON):** Fields to update (`full_name`, `phone`, `education_level`, `academic_percentage`, `field_of_study`, `institution_name`, `annual_income`, `category`, `address`, etc.)
  - **Response `200 OK`:** Updated user object with recalculated `profile_completion`.

---

### 6.2 Saved Scholarships (Bookmarks)
- **Get Bookmarks:** `GET /api/bookmarks`
  - **Access:** Authenticated Student
  - **Response `200 OK`:** Array of bookmarked scholarship objects.
- **Add Bookmark:** `POST /api/bookmarks`
  - **Access:** Authenticated Student
  - **Request Body:** `{"scholarshipId": 3}`
  - **Response `201 Created`:** `{"success": true, "message": "Scholarship saved to bookmarks"}`
- **Delete Bookmark:** `DELETE /api/bookmarks/<scholarship_id>`
  - **Access:** Authenticated Student
  - **Response `200 OK`:** `{"success": true, "message": "Scholarship removed from bookmarks"}`

---

### 6.3 Student Notifications
Retrieves system announcements and status updates for the student.
- **Endpoint:** `GET /api/notifications`
- **Access:** Authenticated Student
- **Response `200 OK`:** Array of notification objects sorted chronologically.

---

## 7. Administrative Management Endpoints

All admin endpoints require an active administrator session.

### 7.1 View All Student Applications
- **Endpoint:** `GET /api/admin/applications`
- **Access:** Authenticated Administrator
- **Query Parameters:** `status` (optional filter, e.g. `Submitted`, `Under Review`, `Approved`, `Rejected`)
- **Response `200 OK`:** Complete list of all student applications including applicant profiles and uploaded documents.

---

### 7.2 Update Application Status & Notes
Updates application status and leaves administrative review feedback.
- **Endpoint:** `PUT /api/admin/applications/<application_id>`
- **Access:** Authenticated Administrator
- **Request Body (JSON):**
  ```json
  {
    "status": "Approved",
    "notes": "All eligibility criteria met. Recommendation forwarded to scholarship disbursements."
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "message": "Application status updated to Approved",
    "application": { ... }
  }
  ```

---

### 7.3 Create Scholarship
- **Endpoint:** `POST /api/admin/scholarships`
- **Access:** Authenticated Administrator
- **Request Body (JSON):**
  ```json
  {
    "name": "State Merit Scholarship 2026",
    "provider": "Department of Higher Education",
    "amount": 50000,
    "category": "Merit-Based",
    "description": "Financial award for top university students.",
    "min_percentage": 75.0,
    "education_levels": "Undergraduate, Postgraduate",
    "eligible_categories": "General, OBC, SC, ST",
    "max_income": 600000,
    "deadline": "2026-12-31",
    "official_url": "https://education.gov.in",
    "official_source": "Ministry of Education",
    "required_documents": "Marksheets, Income Certificate, ID Proof"
  }
  ```
- **Response `201 Created`:** `{"success": true, "scholarshipId": 11, "message": "Scholarship created successfully"}`

---

### 7.4 Update Scholarship
- **Endpoint:** `PUT /api/admin/scholarships/<scholarship_id>`
- **Access:** Authenticated Administrator
- **Request Body (JSON):** Modified fields to update.
- **Response `200 OK`:** `{"success": true, "message": "Scholarship updated successfully"}`

---

### 7.5 Delete Scholarship
- **Endpoint:** `DELETE /api/admin/scholarships/<scholarship_id>`
- **Access:** Authenticated Administrator
- **Response `200 OK`:** `{"success": true, "message": "Scholarship deleted successfully"}`

---

### 7.6 List Registered Students
- **Endpoint:** `GET /api/admin/users`
- **Access:** Authenticated Administrator
- **Response `200 OK`:** List of student profiles (excluding hashed passwords).

---

## 8. Public Contact Inquiries Endpoint

### 8.1 Submit Contact Message
Handles questions, feedback, and support inquiries from the public Contact page.
- **Endpoint:** `POST /api/contact`
- **Access:** Public
- **Request Body (JSON or Form):**
  ```json
  {
    "name": "Priya Nair",
    "email": "priya.nair@example.com",
    "subject": "Inquiry regarding PM-USP Eligibility",
    "message": "Does the PM-USP scholarship cover distance education degrees?"
  }
  ```
- **Response `201 Created`:**
  ```json
  {
    "success": true,
    "message": "Thank you! Your message has been received."
  }
  ```

