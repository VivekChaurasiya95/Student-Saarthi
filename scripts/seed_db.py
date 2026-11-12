import os
import sys
from datetime import datetime, date

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import Admin, User
from app.models.scholarship import Scholarship

def seed_database(app=None):
    """Seed initial administrator and authentic scholarships."""
    if app is None:
        app = create_app()
    with app.app_context():
        db.create_all()
        print("🔧 Checking database tables...")

        # 1. Seed Default Admin
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@studentsaarthi.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Created default admin: username='admin', password='admin123'")
        else:
            print("ℹ️ Admin account already exists.")

        # 2. Seed Authentic Scholarships
        scholarships_data = [
            {
                "id": 1,
                "name": "Mukhyamantri Medhavi Vidyarthi Yojana (MMVY)",
                "provider": "Government of Madhya Pradesh",
                "amount": 150000.0,
                "category": "Academic",
                "description": "Merit-based and need-based financial assistance for meritorious students from Madhya Pradesh who have secured top ranks in Class 12 examinations and are pursuing undergraduate courses in engineering, medicine, law, or recognized universities.",
                "min_percentage": 70.0,
                "education_levels": "Undergraduate",
                "eligible_categories": "General,OBC,SC-ST,Minority",
                "max_income": 600000,
                "age_limit": None,
                "deadline": date(2026, 3, 31),
                "required_documents": "10th Marksheet, 12th Marksheet, Income Certificate, Aadhar Card, Domicile Certificate, Admission Letter, Bank Passbook, Passport Size Photo, Fees Receipt",
                "status": "active",
                "max_applicants": 10000,
                "current_applicants": 1289,
                "official_url": "http://scholarshipportal.mp.nic.in/",
                "official_source": "MP State Scholarship Portal",
                "is_verified": True
            },
            {
                "id": 2,
                "name": "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP)",
                "provider": "Government of India (Central Sector)",
                "amount": 12000.0,
                "category": "Central - Academic",
                "description": "Merit & need-based central scholarship scheme for students above 80th percentile in their relevant stream in Class 12 board examinations pursuing regular graduate / postgraduate courses.",
                "min_percentage": 80.0,
                "education_levels": "Undergraduate,Postgraduate",
                "eligible_categories": "General,OBC,SC-ST,Minority",
                "max_income": 450000,
                "age_limit": None,
                "deadline": date(2026, 2, 28),
                "required_documents": "Caste Certificate, 10th Marksheet, 12th Marksheet, Income Certificate, Aadhar Card, Domicile Certificate, Admission Letter, Bank Passbook, Passport Size Photo, Fees Receipt",
                "status": "active",
                "max_applicants": 15000,
                "current_applicants": 890,
                "official_url": "https://scholarships.gov.in/",
                "official_source": "National Scholarship Portal (NSP)",
                "is_verified": True
            },
            {
                "id": 3,
                "name": "Post Matric Scholarship for Students with Disabilities",
                "provider": "Department of Empowerment of Persons with Disabilities (Central)",
                "amount": 19200.0,
                "category": "Disability",
                "description": "Post-matric educational assistance for students with disability of 40% and above, pursuing recognized post-matric degrees, diplomas, and higher professional education.",
                "min_percentage": 40.0,
                "education_levels": "Class 11,Class 12,Diploma,Undergraduate,Postgraduate",
                "eligible_categories": "General,OBC,SC-ST,Minority,Pwd,Disability",
                "max_income": 250000,
                "age_limit": None,
                "deadline": date(2026, 7, 15),
                "required_documents": "Pwd Certificate, 10th Marksheet, 12th Marksheet, Income Certificate, Aadhar Card, Admission Letter, Bank Passbook, Passport Size Photo, Fees Receipt",
                "status": "active",
                "max_applicants": 1500,
                "current_applicants": 567,
                "official_url": "https://scholarships.gov.in/",
                "official_source": "National Scholarship Portal",
                "is_verified": True
            },
            {
                "id": 4,
                "name": "Pre-Matric Scholarship Scheme for Minorities",
                "provider": "Ministry of Minority Affairs",
                "amount": 42000.0,
                "category": "Minority",
                "description": "Scholarship to encourage parents from minority communities to send their school-going children to school and reduce dropout rates between classes 1 to 10.",
                "min_percentage": 50.0,
                "education_levels": "Class 1,Class 2,Class 3,Class 4,Class 5,Class 6,Class 7,Class 8,Class 9,Class 10",
                "eligible_categories": "Minority",
                "max_income": 100000,
                "age_limit": None,
                "deadline": date(2026, 12, 20),
                "required_documents": "Minority Certificate, 10th Marksheet, Income Certificate, Aadhar Card, Domicile Certificate, Passport Size Photo",
                "status": "active",
                "max_applicants": 1200,
                "current_applicants": 423,
                "official_url": "https://scholarships.gov.in/",
                "official_source": "Ministry of Minority Affairs",
                "is_verified": True
            },
            {
                "id": 5,
                "name": "Post Matric Scholarship Scheme for Scheduled Tribes (ST)",
                "provider": "Ministry of Tribal Affairs",
                "amount": 90000.0,
                "category": "SC-ST",
                "description": "Centrally sponsored scholarship scheme to provide financial assistance to Scheduled Tribe students studying at post-matriculation or post-secondary stage in recognized Indian institutions.",
                "min_percentage": 50.0,
                "education_levels": "Class 11,Class 12,Undergraduate,Postgraduate",
                "eligible_categories": "SC-ST",
                "max_income": 250000,
                "age_limit": None,
                "deadline": date(2026, 1, 15),
                "required_documents": "ST Certificate, 10th Marksheet, 12th Marksheet, Income Certificate, Aadhar Card, Bank Details",
                "status": "active",
                "max_applicants": 5000,
                "current_applicants": 178,
                "official_url": "https://tribal.nic.in/Scholarships.aspx",
                "official_source": "Ministry of Tribal Affairs",
                "is_verified": True
            },
            {
                "id": 6,
                "name": "ICAR Senior Research Fellowship (SRF) — PGS",
                "provider": "Indian Council of Agricultural Research (ICAR)",
                "amount": 103680.0,
                "category": "Research",
                "description": "Prestigious research fellowship awarded on merit through the ICAR All India Competitive Examination to pursue Ph.D. degree programs in agriculture and allied sciences.",
                "min_percentage": 55.0,
                "education_levels": "Postgraduate,PhD",
                "eligible_categories": "General,OBC,SC-ST,Minority",
                "max_income": None,
                "age_limit": 30,
                "deadline": date(2026, 12, 15),
                "required_documents": "Master's Degree Certificate, Admission Proof, Category Certificate, Aadhar Card",
                "status": "active",
                "max_applicants": 6500,
                "current_applicants": 366,
                "official_url": "https://icar.org.in/",
                "official_source": "Indian Council of Agricultural Research",
                "is_verified": True
            },
            {
                "id": 7,
                "name": "Pragati Scholarship Scheme for Girl Students (Technical Degree)",
                "provider": "All India Council for Technical Education (AICTE)",
                "amount": 50000.0,
                "category": "Women",
                "description": "Financial assistance of ₹50,000 per annum towards college fee, computer, books and equipment for girl students admitted to first-year AICTE-approved technical degree programs.",
                "min_percentage": 60.0,
                "education_levels": "Undergraduate",
                "eligible_categories": "General,OBC,SC-ST,Minority,Women",
                "max_income": 800000,
                "age_limit": None,
                "deadline": date(2026, 1, 28),
                "required_documents": "Admission Proof, Category Certificate, Income Certificate, Aadhar Card, Bank Passbook",
                "status": "active",
                "max_applicants": 10000,
                "current_applicants": 4569,
                "official_url": "https://www.aicte-india.org/schemes/students-development-schemes/Pragati",
                "official_source": "AICTE Official Portal",
                "is_verified": True
            },
            {
                "id": 8,
                "name": "HDFC Bank Parivartan Educational Crisis Scholarship Support (ECSS)",
                "provider": "HDFC Bank CSR",
                "amount": 35000.0,
                "category": "Need-Based",
                "description": "Scholarship for meritorious students facing unexpected financial or personal crises that threaten the continuation of their education.",
                "min_percentage": 55.0,
                "education_levels": "Class 10,Class 12,Diploma,Undergraduate,Postgraduate",
                "eligible_categories": "General,OBC,SC-ST,Minority,Pwd",
                "max_income": 250000,
                "age_limit": None,
                "deadline": date(2026, 6, 13),
                "required_documents": "Previous Year Marksheet, Crisis Proof Document, Income Certificate, Aadhar Card, Bank Passbook",
                "status": "active",
                "max_applicants": 25000,
                "current_applicants": 4783,
                "official_url": "https://www.hdfcbank.com/personal/about-us/corporate-social-responsibility",
                "official_source": "HDFC Bank Parivartan",
                "is_verified": True
            },
            {
                "id": 9,
                "name": "National Overseas Scholarship for ST Students",
                "provider": "Ministry of Tribal Affairs",
                "amount": 184800.0,
                "category": "SC-ST",
                "description": "Prestigious support for selected ST candidates admitted to Master's, Ph.D. and post-doctoral research programs in accredited foreign universities.",
                "min_percentage": 60.0,
                "education_levels": "Postgraduate,PhD",
                "eligible_categories": "SC-ST",
                "max_income": 600000,
                "age_limit": 35,
                "deadline": date(2026, 2, 15),
                "required_documents": "ST Certificate, Foreign University Offer Letter, Income Certificate, Passport, Academic Transcripts",
                "status": "active",
                "max_applicants": 50,
                "current_applicants": 14,
                "official_url": "https://overseas.tribal.gov.in/",
                "official_source": "Ministry of Tribal Affairs",
                "is_verified": True
            },
            {
                "id": 10,
                "name": "Reliance Foundation Undergraduate Scholarship",
                "provider": "Reliance Foundation",
                "amount": 200000.0,
                "category": "Academic",
                "description": "Scholarship to support meritorious undergraduate students across India throughout their degree studies, offering up to ₹2 Lakhs along with leadership development programs.",
                "min_percentage": 75.0,
                "education_levels": "Undergraduate",
                "eligible_categories": "General,OBC,SC-ST,Minority",
                "max_income": 1500000,
                "age_limit": None,
                "deadline": date(2026, 2, 15),
                "required_documents": "12th Marksheet, Bonafide Student Certificate, Income Certificate, Aptitude Test Scorecard, Aadhar Card",
                "status": "active",
                "max_applicants": 5000,
                "current_applicants": 1634,
                "official_url": "https://www.scholarships.reliancefoundation.org/",
                "official_source": "Reliance Foundation Education",
                "is_verified": True
            }
        ]

        loaded_count = 0
        for item in scholarships_data:
            sch = Scholarship.query.filter_by(name=item['name']).first()
            if not sch:
                sch = Scholarship(
                    id=item['id'],
                    name=item['name'],
                    provider=item['provider'],
                    amount=item['amount'],
                    category=item['category'],
                    description=item['description'],
                    min_percentage=item['min_percentage'],
                    education_levels=item['education_levels'],
                    eligible_categories=item['eligible_categories'],
                    max_income=item['max_income'],
                    age_limit=item['age_limit'],
                    deadline=item['deadline'],
                    required_documents=item['required_documents'],
                    status=item['status'],
                    max_applicants=item['max_applicants'],
                    current_applicants=item['current_applicants'],
                    official_url=item['official_url'],
                    official_source=item['official_source'],
                    is_verified=item['is_verified']
                )
                db.session.add(sch)
                loaded_count += 1

        db.session.commit()
        print(f"✅ Loaded {loaded_count} new scholarships into database (Total: {Scholarship.query.count()})")
        print("🎉 Database seeding complete!")

if __name__ == '__main__':
    seed_database()

