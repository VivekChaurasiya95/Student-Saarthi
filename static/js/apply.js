// Student Saarthi - Executive Application Form Engine
var API_URL = window.API_URL || (window.location.origin + '/api');

let currentScholarship = null;
let userProfile = null;

// Verify session and role
async function checkAuth() {
    try {
        const data = window.getAppSession 
            ? await window.getAppSession() 
            : await (await fetch(`${API_URL}/check-session`, { credentials: 'include' })).json();
        if (!data || !data.loggedIn || data.type !== 'user') {
            window.location.href = '/login.html';
            return false;
        }
        return true;
    } catch (e) {
        window.location.href = '/login.html';
        return false;
    }
}

// Load Scholarship & Profile
async function loadScholarshipAndProfile() {
    const urlParams = new URLSearchParams(window.location.search);
    const scholarshipId = urlParams.get('id');

    if (!scholarshipId) {
        window.location.href = '/scholarships.html';
        return;
    }

    try {
        // Fetch target scholarship details
        const schRes = await fetch(`${API_URL}/scholarships/${scholarshipId}`);
        if (!schRes.ok) throw new Error('Scholarship opportunity not found');
        currentScholarship = await schRes.json();

        // Fetch verified student profile
        const profRes = await fetch(`${API_URL}/profile`, { credentials: 'include' });
        if (!profRes.ok) throw new Error('Failed to retrieve student profile');
        userProfile = await profRes.json();

        // Render scholarship metadata header
        document.getElementById('scholarshipName').textContent = currentScholarship.name;
        document.getElementById('scholarshipProvider').textContent = currentScholarship.provider;
        const amountVal = parseFloat(currentScholarship.amount || 0);
        document.getElementById('scholarshipAmount').textContent = amountVal > 0 ? `₹${amountVal.toLocaleString('en-IN')}` : 'Full Funding';

        // Render required documents checklist
        const docsList = document.getElementById('documentsList');
        if (currentScholarship.required_documents) {
            const docs = currentScholarship.required_documents.split(',');
            docsList.innerHTML = docs.map(d => `<li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>${d.trim()}</li>`).join('');
        } else {
            docsList.innerHTML = `
                <li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Academic Qualifying Examination Marksheet</li>
                <li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Government Photo Identity Card (Aadhaar / Voter ID)</li>
                <li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Annual Family Income Certificate</li>
            `;
        }

        // Prepopulate profile identity details
        document.getElementById('fullName').value = userProfile.full_name || '';
        document.getElementById('email').value = userProfile.email || '';
        document.getElementById('phone').value = userProfile.phone || '';
        document.getElementById('educationLevel').value = userProfile.education_level || 'Undergraduate';

        // Run automated eligibility audit
        checkEligibility();
    } catch (error) {
        console.error('Error loading data:', error);
        if (window.Swal) {
            Swal.fire({
                icon: 'error',
                title: 'Unable To Load Program',
                text: 'The requested scholarship program could not be loaded. Returning to directory.',
                confirmButtonColor: '#2563eb'
            }).then(() => {
                window.location.href = '/scholarships.html';
            });
        }
    }
}

// Evaluate eligibility parameters
function checkEligibility() {
    const resultsContainer = document.getElementById('eligibilityResults');
    if (!resultsContainer || !currentScholarship || !userProfile) return;

    const checks = [];
    let isFullyEligible = true;

    // Academic Score Cutoff
    if (currentScholarship.min_percentage) {
        const studentPct = parseFloat(userProfile.academic_percentage || 0);
        const passed = studentPct >= currentScholarship.min_percentage;
        checks.push({
            label: `Minimum ${currentScholarship.min_percentage}% Academic Cutoff`,
            status: passed,
            detail: `Your Profile Score: ${studentPct}%`
        });
        if (!passed) isFullyEligible = false;
    }

    // Education Level Check
    if (currentScholarship.education_levels) {
        const studentLevel = (userProfile.education_level || '').trim();
        const passed = currentScholarship.education_levels.toLowerCase().includes(studentLevel.toLowerCase());
        checks.push({
            label: `Permitted Education Levels: ${currentScholarship.education_levels}`,
            status: passed,
            detail: `Your Current Enrolled Level: ${studentLevel || 'Not configured'}`
        });
        if (!passed) isFullyEligible = false;
    }

    // Reservation Category Check
    if (currentScholarship.eligible_categories) {
        const studentCat = (userProfile.category || '').trim();
        const passed = currentScholarship.eligible_categories.toLowerCase().includes(studentCat.toLowerCase());
        checks.push({
            label: `Eligible Categories: ${currentScholarship.eligible_categories}`,
            status: passed,
            detail: `Your Reservation Category: ${studentCat || 'General'}`
        });
        if (!passed) isFullyEligible = false;
    }

    // Income Ceiling Check
    if (currentScholarship.max_income) {
        const studentIncome = parseInt(userProfile.annual_income || 0);
        const passed = studentIncome > 0 && studentIncome <= currentScholarship.max_income;
        checks.push({
            label: `Family Income Cap: Under ₹${parseFloat(currentScholarship.max_income).toLocaleString('en-IN')}`,
            status: passed,
            detail: `Your Declared Income: ₹${studentIncome.toLocaleString('en-IN')}`
        });
        if (!passed) isFullyEligible = false;
    }

    resultsContainer.innerHTML = checks.map(c => `
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 12px; background: var(--surface-color); padding: 12px 16px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <i class="fas fa-${c.status ? 'circle-check' : 'circle-xmark'}" 
               style="color: var(--${c.status ? 'emerald-accent' : 'error-color'}); font-size: 20px;"></i>
            <div style="flex: 1;">
                <div style="font-weight: 700; color: var(--text-primary); font-size: 13.5px;">${c.label}</div>
                <div style="font-size: 12.5px; color: var(--text-secondary); margin-top: 2px;">${c.detail}</div>
            </div>
            <span class="status-pill ${c.status ? 'status-approved' : 'status-rejected'}" style="font-size: 11px;">
                ${c.status ? 'Satisfied' : 'Review Required'}
            </span>
        </div>
    `).join('');

    if (!isFullyEligible) {
        resultsContainer.innerHTML += `
            <div style="background: rgba(217, 119, 6, 0.08); padding: 14px 18px; border-radius: var(--radius-md); margin-top: 14px; border: 1px solid rgba(217, 119, 6, 0.25);">
                <p style="color: var(--gold-accent); font-weight: 600; margin: 0; font-size: 13.5px;">
                    <i class="fas fa-triangle-exclamation" style="margin-right: 6px;"></i>
                    Note: You may be on the threshold of strict criteria. You can still submit your dossier for manual committee evaluation.
                </p>
            </div>
        `;
    } else {
        resultsContainer.innerHTML += `
            <div style="background: rgba(5, 150, 105, 0.08); padding: 14px 18px; border-radius: var(--radius-md); margin-top: 14px; border: 1px solid rgba(5, 150, 105, 0.25);">
                <p style="color: var(--emerald-accent); font-weight: 600; margin: 0; font-size: 13.5px;">
                    <i class="fas fa-certificate" style="margin-right: 6px;"></i>
                    Eligibility Cleared: Your profile meets or exceeds all criteria for direct consideration.
                </p>
            </div>
        `;
    }
}

// Form Submission with SweetAlert2
document.addEventListener('DOMContentLoaded', async () => {
    const isAuth = await checkAuth();
    if (isAuth) {
        await loadScholarshipAndProfile();
    }

    const appForm = document.getElementById('applicationForm');
    if (appForm) {
        appForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const sop = document.getElementById('sop').value.trim();
            if (sop.length < 50) {
                window.showToast('Statement of Purpose must be at least 50 characters', 'warning');
                return;
            }

            if (!document.getElementById('agreeTerms').checked) {
                window.showToast('Please confirm the accuracy declaration', 'warning');
                return;
            }

            const urlParams = new URLSearchParams(window.location.search);
            const scholarshipId = urlParams.get('id');

            const submitBtn = appForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Submitting Application Dossier...';

            const formData = new FormData();
            formData.append('scholarshipId', scholarshipId);
            formData.append('sop', sop);
            formData.append('achievements', document.getElementById('achievements')?.value || '');
            formData.append('extracurricular', document.getElementById('extracurricular')?.value || '');
            formData.append('additionalInfo', document.getElementById('additionalInfo')?.value || '');

            const fileInput = document.getElementById('documents');
            if (fileInput && fileInput.files.length > 0) {
                for (let i = 0; i < fileInput.files.length; i++) {
                    formData.append('documents', fileInput.files[i]);
                }
            }

            try {
                const response = await fetch(`${API_URL}/apply`, {
                    method: 'POST',
                    credentials: 'include',
                    body: formData
                });

                const data = await response.json();
                if (response.ok && data.success) {
                    if (window.Swal) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Application Submitted!',
                            text: `Your dossier has been registered under Application Reference #${data.applicationId.substring(0, 8).toUpperCase()}.`,
                            confirmButtonColor: '#2563eb',
                            confirmButtonText: 'View My Applications'
                        }).then(() => {
                            window.location.href = '/my-application.html';
                        });
                    } else {
                        window.showToast('Application submitted successfully!', 'success');
                        setTimeout(() => {
                            window.location.href = '/my-application.html';
                        }, 1500);
                    }
                } else {
                    window.showToast(data.error || 'Failed to submit application', 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Application Dossier';
                }
            } catch (err) {
                console.error('Submission error:', err);
                window.showToast('Server connection failed. Please retry.', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Application Dossier';
            }
        });
    }
});
