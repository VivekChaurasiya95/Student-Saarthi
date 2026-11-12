// Student Saarthi - Executive Application Tracking Engine
var API_URL = window.API_URL || (window.location.origin + '/api');

let studentApplications = [];

// Verify student session
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

// Map status string to custom luxury badge classes
function getStatusBadge(status) {
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

// Load applications from backend
async function loadApplications() {
    try {
        const response = await fetch(`${API_URL}/applications`, { credentials: 'include' });
        if (!response.ok) throw new Error('Failed to fetch applications');
        
        studentApplications = await response.json();

        // Count status tallies
        const counts = {
            'Submitted': 0,
            'Under Review': 0,
            'Approved': 0,
            'Rejected': 0
        };

        studentApplications.forEach(app => {
            const st = app.application_status;
            if (counts.hasOwnProperty(st)) {
                counts[st]++;
            } else if (st === 'Additional Information Required') {
                counts['Under Review']++;
            } else {
                counts['Submitted']++;
            }
        });

        document.getElementById('submittedCount').textContent = counts['Submitted'];
        document.getElementById('reviewCount').textContent = counts['Under Review'];
        document.getElementById('approvedCount').textContent = counts['Approved'];
        document.getElementById('rejectedCount').textContent = counts['Rejected'];

        const counterPill = document.getElementById('applicationsCounter');
        if (counterPill) {
            counterPill.textContent = `${studentApplications.length} Total Submissions`;
        }

        renderApplicationsTable(studentApplications);
    } catch (error) {
        console.error('Error loading applications:', error);
        const tbody = document.getElementById('applicationsTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 48px; color: var(--error-color);">
                        <i class="fas fa-circle-exclamation" style="font-size: 32px; margin-bottom: 8px;"></i>
                        <p style="margin: 0; font-weight: 600;">Unable to connect to application database.</p>
                    </td>
                </tr>
            `;
        }
    }
}

// Render table rows
function renderApplicationsTable(applications) {
    const tableBody = document.getElementById('applicationsTable');
    if (!tableBody) return;

    if (applications.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 60px 20px;">
                    <div class="feature-icon-box" style="margin: 0 auto 16px; width: 60px; height: 60px; font-size: 24px;">
                        <i class="fas fa-folder-open"></i>
                    </div>
                    <h3 style="margin-bottom: 8px;">No Application Dossiers Found</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 24px; max-width: 440px; margin-left: auto; margin-right: auto;">
                        You have not submitted any scholarship applications yet. Browse verified opportunities and submit your profile.
                    </p>
                    <a href="/scholarships.html" class="btn btn-primary">
                        <i class="fas fa-compass"></i> Discover Scholarships
                    </a>
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

        const amountFormatted = parseFloat(app.amount || 0).toLocaleString('en-IN');
        const statusHtml = getStatusBadge(app.application_status);

        return `
            <tr>
                <td>
                    <span style="font-family: monospace; font-weight: 700; color: var(--brand-blue); background: rgba(37,99,235,0.08); padding: 4px 8px; border-radius: var(--radius-sm);">
                        #${app.id.substring(0, 8).toUpperCase()}
                    </span>
                </td>
                <td>
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 14.5px;">${app.scholarship_name || 'Scholarship Grant'}</div>
                    <div style="color: var(--text-muted); font-size: 12.5px; margin-top: 2px;">
                        <i class="fas fa-building-columns" style="font-size: 11px;"></i> ${app.provider || 'State Department'}
                    </div>
                </td>
                <td>
                    <strong style="color: var(--text-primary); font-size: 15px;">₹${amountFormatted}</strong>
                </td>
                <td style="color: var(--text-secondary); font-size: 13.5px;">${appliedDate}</td>
                <td>
                    ${statusHtml}
                    ${app.admin_notes ? `<div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px; font-style: italic;"><i class="fas fa-comment-dots" style="color: var(--brand-blue);"></i> "${app.admin_notes}"</div>` : ''}
                </td>
                <td style="text-align: right;">
                    <button class="btn btn-sm btn-outline" onclick="viewApplicationDetail('${app.id}')">
                        <i class="fas fa-file-lines"></i> Inspect
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// View application detail in modern modal
function viewApplicationDetail(appId) {
    const app = studentApplications.find(a => a.id === appId);
    if (!app) return;

    const modalBody = document.getElementById('appDetailModalBody');
    if (!modalBody) return;

    const appliedDate = app.applied_date ? new Date(app.applied_date).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    }) : 'Pending';

    const statusHtml = getStatusBadge(app.application_status);
    const amountFormatted = parseFloat(app.amount || 0).toLocaleString('en-IN');

    modalBody.innerHTML = `
        <div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 20px;">
                <div>
                    <h3 style="font-size: 1.35rem; color: var(--text-primary); margin-bottom: 6px;">${app.scholarship_name}</h3>
                    <p style="color: var(--text-secondary); font-size: 13.5px; margin: 0;">
                        Tracking Reference: <strong style="font-family: monospace; color: var(--brand-blue);">#${app.id}</strong>
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.7rem; font-weight: 800; color: var(--text-primary);">₹${amountFormatted}</div>
                    <div style="margin-top: 4px;">${statusHtml}</div>
                </div>
            </div>

            <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 16px; margin-bottom: 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px;">
                <div>
                    <span style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Submission Date</span>
                    <p style="font-size: 14px; font-weight: 600; margin: 4px 0 0; color: var(--text-primary);">${appliedDate}</p>
                </div>
                <div>
                    <span style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Sanctioning Body</span>
                    <p style="font-size: 14px; font-weight: 600; margin: 4px 0 0; color: var(--text-primary);">${app.provider || 'State Government'}</p>
                </div>
            </div>

            <h4 style="margin-bottom: 8px; font-size: 1.05rem;">Statement of Purpose:</h4>
            <div style="background: var(--surface-color); border: 1px solid var(--border-color); padding: 16px; border-radius: var(--radius-md); margin-bottom: 20px;">
                <p style="white-space: pre-wrap; margin: 0; font-size: 14px; line-height: 1.7; color: var(--text-primary);">${app.statement_of_purpose || 'No statement provided.'}</p>
            </div>

            ${app.academic_achievements ? `
                <h4 style="margin-bottom: 8px; font-size: 1.05rem;">Honors & Achievements:</h4>
                <div style="background: var(--surface-color); border: 1px solid var(--border-color); padding: 16px; border-radius: var(--radius-md); margin-bottom: 20px;">
                    <p style="white-space: pre-wrap; margin: 0; font-size: 14px; line-height: 1.7; color: var(--text-primary);">${app.academic_achievements}</p>
                </div>
            ` : ''}

            ${app.admin_notes ? `
                <div style="background: rgba(37, 99, 235, 0.06); border: 1px solid rgba(37, 99, 235, 0.2); padding: 16px; border-radius: var(--radius-md); margin-top: 24px;">
                    <div style="font-size: 12.5px; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; margin-bottom: 4px;">
                        <i class="fas fa-shield-halved"></i> Review Committee Remarks
                    </div>
                    <p style="margin: 0; font-size: 14px; color: var(--text-primary); font-weight: 500;">${app.admin_notes}</p>
                </div>
            ` : ''}

            <div style="margin-top: 28px; text-align: right;">
                <button class="btn btn-outline" onclick="closeAppDetailModal()">Close Overview</button>
            </div>
        </div>
    `;

    const modal = document.getElementById('appDetailModal');
    if (modal) modal.classList.add('active');
}

function closeAppDetailModal() {
    const modal = document.getElementById('appDetailModal');
    if (modal) modal.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', async () => {
    const isAuth = await checkAuth();
    if (isAuth) {
        loadApplications();
    }

    const modal = document.getElementById('appDetailModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.id === 'appDetailModal') closeAppDetailModal();
        });
    }
});
