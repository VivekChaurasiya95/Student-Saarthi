// Student Saarthi - Executive Admin Control Center Engine
var API_URL = window.API_URL || (window.location.origin + '/api');

let adminChartInstance = null;

// Verify Administrator Authentication
async function checkAdminAuth() {
    try {
        const data = window.getAppSession 
            ? await window.getAppSession() 
            : await (await fetch(`${API_URL}/check-session`, { credentials: 'include' })).json();
        
        if (!data || !data.loggedIn || data.type !== 'admin') {
            window.location.href = '/login.html?admin=true';
            return false;
        }

        const nameEl = document.getElementById('adminName');
        if (nameEl) nameEl.textContent = data.username || 'Administrator';
        return true;
    } catch (e) {
        console.error('Admin auth check error:', e);
        window.location.href = '/login.html?admin=true';
        return false;
    }
}

// Map status to badges
function getAdminStatusBadge(status) {
    const s = (status || '').toLowerCase().replace(/\s+/g, '-');
    if (s.includes('approve') || s.includes('sanction')) {
        return `<span class="status-pill status-approved"><i class="fas fa-circle-check"></i> ${status}</span>`;
    }
    if (s.includes('review') || s.includes('additional')) {
        return `<span class="status-pill status-under-review"><i class="fas fa-hourglass-half"></i> ${status}</span>`;
    }
    if (s.includes('reject') || s.includes('decline')) {
        return `<span class="status-pill status-rejected"><i class="fas fa-circle-xmark"></i> ${status}</span>`;
    }
    return `<span class="status-pill status-submitted"><i class="fas fa-paper-plane"></i> ${status || 'Submitted'}</span>`;
}

// Render Administrative Chart.js Visualizer
function renderAdminChart(submitted, underReview, approved, rejected) {
    const ctx = document.getElementById('adminAnalyticsChart');
    if (!ctx || !window.Chart) return;

    if (adminChartInstance) {
        adminChartInstance.destroy();
    }

    adminChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Submitted & Queued', 'Under Review', 'Sanctioned / Approved', 'Declined / Rejected'],
            datasets: [{
                label: 'Candidate Applications',
                data: [submitted, underReview, approved, rejected],
                backgroundColor: [
                    'rgba(37, 99, 235, 0.85)',
                    'rgba(217, 119, 6, 0.85)',
                    'rgba(5, 150, 105, 0.85)',
                    'rgba(220, 38, 38, 0.85)'
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0, font: { family: 'Plus Jakarta Sans', size: 12 } },
                    grid: { color: 'rgba(148, 163, 184, 0.15)' }
                },
                x: {
                    ticks: { font: { family: 'Plus Jakarta Sans', size: 12 } },
                    grid: { display: false }
                }
            }
        }
    });
}

// Load Admin Dashboard Telemetry
async function loadAdminDashboard() {
    try {
        const [scholarshipsRes, usersRes, applicationsRes] = await Promise.all([
            fetch(`${API_URL}/scholarships`, { credentials: 'include' }),
            fetch(`${API_URL}/admin/users`, { credentials: 'include' }),
            fetch(`${API_URL}/admin/applications`, { credentials: 'include' })
        ]);

        if (!scholarshipsRes.ok || !usersRes.ok || !applicationsRes.ok) {
            throw new Error('Failed to fetch admin dashboard telemetry');
        }

        const scholarships = await scholarshipsRes.json();
        const users = await usersRes.json();
        const applications = await applicationsRes.json();

        // Update statistics cards
        document.getElementById('totalScholarships').textContent = scholarships.length;
        document.getElementById('totalStudents').textContent = users.length;
        document.getElementById('totalApplications').textContent = applications.length;

        const counterPill = document.getElementById('adminAppCounter');
        if (counterPill) {
            counterPill.textContent = `${applications.length} Submissions Logged`;
        }

        let submitted = 0;
        let underReview = 0;
        let approved = 0;
        let rejected = 0;

        applications.forEach(a => {
            const st = (a.application_status || '').toLowerCase();
            if (st.includes('approve')) approved++;
            else if (st.includes('reject') || st.includes('decline')) rejected++;
            else if (st.includes('review') || st.includes('additional')) underReview++;
            else submitted++;
        });

        document.getElementById('pendingApplications').textContent = submitted + underReview;

        renderAdminChart(submitted, underReview, approved, rejected);
        displayApplicationsTable(applications);
    } catch (error) {
        console.error('Admin dashboard error:', error);
    }
}

// Render Applications Table
function displayApplicationsTable(applications) {
    const tableBody = document.getElementById('applicationsTable');
    if (!tableBody) return;

    if (applications.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 48px;">
                    <i class="fas fa-inbox" style="font-size: 40px; color: var(--text-muted); margin-bottom: 12px;"></i>
                    <h4 style="margin-bottom: 6px;">No Applications In Queue</h4>
                    <p style="color: var(--text-secondary); margin: 0; font-size: 14px;">Submitted candidate dossiers will populate here for evaluation.</p>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = applications.map(app => {
        const appliedDate = app.applied_date ? new Date(app.applied_date).toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        }) : '-';

        const amtFormatted = parseFloat(app.amount || 0).toLocaleString('en-IN');
        const statusBadge = getAdminStatusBadge(app.application_status);

        return `
            <tr>
                <td>
                    <span style="font-family: monospace; font-weight: 700; color: var(--brand-blue); background: rgba(37,99,235,0.08); padding: 4px 8px; border-radius: var(--radius-sm);">
                        #${app.id.substring(0, 8).toUpperCase()}
                    </span>
                </td>
                <td>
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 14px;">${app.student_name || 'Scholar Candidate'}</div>
                    <div style="color: var(--text-secondary); font-size: 12.5px; margin-top: 2px;">
                        <i class="fas fa-envelope" style="font-size: 11px;"></i> ${app.student_email || 'No email'}
                    </div>
                </td>
                <td>
                    <div style="font-weight: 600; color: var(--text-primary); font-size: 14px;">${app.scholarship_name || 'Scholarship'}</div>
                    <div style="color: var(--text-muted); font-size: 12.5px; margin-top: 2px;">₹${amtFormatted} Grant</div>
                </td>
                <td style="color: var(--text-secondary); font-size: 13.5px;">${appliedDate}</td>
                <td>${statusBadge}</td>
                <td style="text-align: right;">
                    <select onchange="updateApplicationStatus('${app.id}', this.value)" 
                            style="padding: 7px 12px; border-radius: var(--radius-md); font-size: 13px; font-weight: 600; border: 1px solid var(--border-color); background: var(--surface-color); color: var(--text-primary); cursor: pointer;">
                        <option value="Submitted" ${app.application_status === 'Submitted' ? 'selected' : ''}>Submitted</option>
                        <option value="Under Review" ${app.application_status === 'Under Review' ? 'selected' : ''}>Under Review</option>
                        <option value="Approved" ${app.application_status === 'Approved' ? 'selected' : ''}>Approved</option>
                        <option value="Rejected" ${app.application_status === 'Rejected' ? 'selected' : ''}>Rejected</option>
                    </select>
                </td>
            </tr>
        `;
    }).join('');
}

// Update Application Status with SweetAlert2
async function updateApplicationStatus(applicationId, newStatus) {
    try {
        const response = await fetch(`${API_URL}/admin/applications/${applicationId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ status: newStatus })
        });
        const data = await response.json();
        if (response.ok) {
            window.showToast(`Status updated to ${newStatus}`, 'success');
            loadAdminDashboard();
        } else {
            window.showToast(data.error || 'Failed to update application status', 'error');
        }
    } catch (e) {
        console.error('Update status error:', e);
        window.showToast('Network error while updating status', 'error');
    }
}

// Modal handling for Add Scholarship
function showAddScholarshipModal() {
    const modal = document.getElementById('addScholarshipModal');
    if (modal) modal.classList.add('active');
}

function closeAddScholarshipModal() {
    const modal = document.getElementById('addScholarshipModal');
    if (modal) modal.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', async () => {
    const isAuth = await checkAdminAuth();
    if (isAuth) {
        loadAdminDashboard();
    }

    const addForm = document.getElementById('addScholarshipForm');
    if (addForm) {
        addForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const scholarshipPayload = {
                name: document.getElementById('schName').value.trim(),
                provider: document.getElementById('schProvider').value.trim(),
                amount: parseFloat(document.getElementById('schAmount').value),
                category: document.getElementById('schCategory').value.trim(),
                minPercentage: parseFloat(document.getElementById('schMinPercentage').value || 0),
                description: document.getElementById('schDescription').value.trim(),
                educationLevels: document.getElementById('schEducation').value.trim(),
                deadline: document.getElementById('schDeadline').value,
                requiredDocuments: document.getElementById('schDocuments').value.trim(),
                maxIncome: parseInt(document.getElementById('schMaxIncome')?.value || 0) || null,
                officialUrl: document.getElementById('schOfficialUrl')?.value.trim() || ''
            };

            const submitBtn = addForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Authoring Scheme...';

            try {
                const response = await fetch(`${API_URL}/admin/scholarships`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify(scholarshipPayload)
                });

                const data = await response.json();
                if (response.ok) {
                    window.showToast('Scholarship scheme published successfully!', 'success');
                    closeAddScholarshipModal();
                    addForm.reset();
                    loadAdminDashboard();
                } else {
                    window.showToast(data.error || 'Failed to add scholarship', 'error');
                }
            } catch (err) {
                console.error('Add scholarship error:', err);
                window.showToast('Network error while adding scholarship', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-plus"></i> Publish Scholarship Scheme';
            }
        });
    }

    const modal = document.getElementById('addScholarshipModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.id === 'addScholarshipModal') closeAddScholarshipModal();
        });
    }
});
