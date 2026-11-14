// Student Saarthi - Executive Student Dashboard Engine
var API_URL = window.API_URL || (window.location.origin + '/api');

let currentProfile = null;
let allScholarships = [];
let applicationsChartInstance = null;

// Verify student authentication
async function checkAuth() {
    try {
        const data = window.getAppSession 
            ? await window.getAppSession() 
            : await (await fetch(`${API_URL}/check-session`, { credentials: 'include' })).json();

        if (!data || !data.loggedIn || data.type !== 'user') {
            window.location.href = '/login.html';
            return false;
        }

        const nameEl = document.getElementById('userName');
        if (nameEl) nameEl.textContent = data.userName || 'Scholar';
        return true;
    } catch (error) {
        console.error('Session authentication error:', error);
        window.location.href = '/login.html';
        return false;
    }
}

// Category Badge Helper
function getCategoryBadgeClass(category) {
    const cat = (category || '').toLowerCase();
    if (cat.includes('merit') || cat.includes('academic')) return 'badge-academic';
    if (cat.includes('need') || cat.includes('income') || cat.includes('means')) return 'badge-need';
    if (cat.includes('women') || cat.includes('girl')) return 'badge-women';
    return 'badge-general';
}

// Render Doughnut Chart using Chart.js
function renderApplicationsChart(submitted, underReview, approved, bookmarked) {
    const ctx = document.getElementById('applicationsChart');
    if (!ctx || !window.Chart) return;

    if (applicationsChartInstance) {
        applicationsChartInstance.destroy();
    }

    const totalActive = submitted + underReview;
    const activeEl = document.getElementById('chartActiveStat');
    const approvedEl = document.getElementById('chartApprovedStat');
    const savedEl = document.getElementById('chartSavedStat');
    if (activeEl) activeEl.textContent = totalActive;
    if (approvedEl) approvedEl.textContent = approved;
    if (savedEl) savedEl.textContent = bookmarked;

    const hasData = (submitted + underReview + approved + bookmarked) > 0;
    const dataValues = hasData ? [submitted, underReview, approved, bookmarked] : [1, 0, 0, 0];
    const dataColors = hasData ? ['#2563eb', '#d97706', '#059669', '#64748b'] : ['#e2e8f0', '#cbd5e1', '#94a3b8', '#64748b'];

    applicationsChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Submitted', 'Under Review', 'Approved', 'Bookmarked'],
            datasets: [{
                data: dataValues,
                backgroundColor: dataColors,
                borderWidth: 0,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: hasData
                }
            },
            cutout: '72%'
        }
    });
}

// Load Dashboard Telemetry & Data
async function loadDashboardData() {
    try {
        let appCounts = { submitted: 0, underReview: 0, approved: 0 };
        let bookmarkedCount = 0;

        // 1. Total Catalog Count
        const statsRes = await fetch(`${API_URL}/stats`);
        if (statsRes.ok) {
            const stats = await statsRes.json();
            const totalSchEl = document.getElementById('totalScholarships');
            if (totalSchEl) totalSchEl.textContent = (stats.scholarships || 10) + '+';
        }

        // 2. Load Applications
        const appsRes = await fetch(`${API_URL}/applications`, { credentials: 'include' });
        if (appsRes.ok) {
            const apps = await appsRes.json();
            const myAppsEl = document.getElementById('myApplications');
            if (myAppsEl) myAppsEl.textContent = apps.length;

            apps.forEach(a => {
                const st = (a.application_status || '').toLowerCase();
                if (st.includes('approve')) appCounts.approved++;
                else if (st.includes('review') || st.includes('additional')) appCounts.underReview++;
                else appCounts.submitted++;
            });
        }

        // 3. Load Bookmarks
        const bookRes = await fetch(`${API_URL}/bookmarks`, { credentials: 'include' });
        if (bookRes.ok) {
            const bookmarks = await bookRes.json();
            bookmarkedCount = bookmarks.length;
            const bookCountEl = document.getElementById('bookmarkedScholarships');
            if (bookCountEl) bookCountEl.textContent = bookmarks.length;
            renderScholarshipsGrid('bookmarkedList', bookmarks, true);
        }

        // 4. Initialize Chart
        renderApplicationsChart(appCounts.submitted, appCounts.underReview, appCounts.approved, bookmarkedCount);

        // 5. Load Profile & Recommendations
        const profRes = await fetch(`${API_URL}/profile`, { credentials: 'include' });
        if (profRes.ok) {
            currentProfile = await profRes.json();
            const pctEl = document.getElementById('profileCompletion');
            if (pctEl) {
                pctEl.textContent = (currentProfile.profile_completion || 85) + '%';
            }
            await loadRecommendedScholarships(currentProfile);
        }
    } catch (e) {
        console.error('Dashboard data load error:', e);
    }
}

// Load tailored recommendations based on profile
async function loadRecommendedScholarships(profile) {
    try {
        const response = await fetch(`${API_URL}/scholarships`);
        if (!response.ok) return;

        allScholarships = await response.json();

        const studentPct = parseFloat(profile.academic_percentage || 0);
        const studentCat = (profile.category || '').toLowerCase();
        const studentIncome = parseInt(profile.annual_income || 999999999);

        const recommended = allScholarships.filter(s => {
            if (s.min_percentage && studentPct > 0 && studentPct < s.min_percentage) {
                return false;
            }
            if (s.eligible_categories && studentCat) {
                const catLower = s.eligible_categories.toLowerCase();
                if (!catLower.includes(studentCat) && !catLower.includes('general') && !catLower.includes('all')) {
                    return false;
                }
            }
            if (s.max_income && studentIncome > 0 && studentIncome > s.max_income) {
                return false;
            }
            return true;
        }).slice(0, 6);

        renderScholarshipsGrid('recommendedScholarships', recommended, false);
    } catch (e) {
        console.error('Recommendations error:', e);
    }
}

// Render luxury bento scholarship cards
function renderScholarshipsGrid(containerId, scholarships, isBookmarkList) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!scholarships || scholarships.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 48px;">
                <div class="feature-icon-box" style="margin: 0 auto 16px; width: 56px; height: 56px; font-size: 22px;">
                    <i class="fas fa-folder-open"></i>
                </div>
                <h4 style="margin-bottom: 6px;">${isBookmarkList ? 'No Saved Scholarships' : 'No Tailored Matches Yet'}</h4>
                <p style="color: var(--text-secondary); margin: 0; font-size: 14px;">
                    ${isBookmarkList ? 'Save programs from the discovery directory to build your personalized application queue.' : 'Update your profile marks or category to unlock tailored grant matches.'}
                </p>
            </div>
        `;
        return;
    }

    container.innerHTML = scholarships.map(s => {
        const amt = parseFloat(s.amount || 0).toLocaleString('en-IN');
        const badgeClass = getCategoryBadgeClass(s.category);
        return `
            <div class="scholarship-card">
                <div class="scholarship-header">
                    <div>
                        <div class="scholarship-amount-tag">₹${amt}</div>
                        <div class="scholarship-amount-sub">Grant Allowance</div>
                    </div>
                    <span class="scholarship-badge ${badgeClass}">${s.category || 'General'}</span>
                </div>
                <div class="scholarship-body">
                    <h3>${s.name}</h3>
                    <p class="scholarship-provider">
                        <i class="fas fa-building-columns"></i> ${s.provider}
                    </p>
                    <p class="scholarship-description">${(s.description || 'Verified educational aid program for qualified scholars.').substring(0, 110)}...</p>
                    <div class="scholarship-meta-pills">
                        <span class="meta-pill"><i class="fas fa-graduation-cap"></i> ${s.education_levels ? s.education_levels.split(',')[0].trim() : 'Higher Ed'}</span>
                        <span class="meta-pill"><i class="fas fa-percent"></i> ${s.min_percentage ? s.min_percentage + '% min' : 'Merit'}</span>
                    </div>
                </div>
                <div class="scholarship-footer">
                    <a href="/apply?id=${s.id}" class="btn btn-primary btn-sm">
                        Apply Now <i class="fas fa-chevron-right" style="font-size: 11px;"></i>
                    </a>
                    ${isBookmarkList ? `
                        <button class="btn-bookmark bookmarked" onclick="removeBookmark(${s.id})" title="Remove from wishlist">
                            <i class="fas fa-trash-can" style="color: var(--error-color);"></i>
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Remove bookmark
async function removeBookmark(scholarshipId) {
    try {
        const response = await fetch(`${API_URL}/bookmarks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ scholarshipId })
        });
        if (response.ok) {
            window.showToast('Bookmark removed from your wishlist', 'info');
            loadDashboardData();
        }
    } catch (e) {
        window.showToast('Failed to remove bookmark', 'error');
    }
}

// Show Eligibility Checker Modal
function showEligibilityChecker() {
    const modal = document.getElementById('eligibilityModal');
    const resultsContainer = document.getElementById('eligibilityResults');
    if (!modal || !resultsContainer) return;

    if (!currentProfile) {
        resultsContainer.innerHTML = '<p style="color: var(--error-color);">Profile details not loaded yet. Please reload.</p>';
        if (window.openModalById) {
            window.openModalById('eligibilityModal');
        } else {
            modal.classList.add('active');
        }
        return;
    }

    const marks = currentProfile.academic_percentage || 0;
    const cat = currentProfile.category || 'General';
    const income = parseInt(currentProfile.annual_income || 0);

    resultsContainer.innerHTML = `
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 24px;">
            <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em;">Current Profile Dossier</span>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-top: 10px;">
                <div>
                    <div style="font-size: 12px; color: var(--text-muted);">Academic Score</div>
                    <div style="font-size: 16px; font-weight: 800; color: var(--text-primary);">${marks}%</div>
                </div>
                <div>
                    <div style="font-size: 12px; color: var(--text-muted);">Category</div>
                    <div style="font-size: 16px; font-weight: 800; color: var(--text-primary);">${cat}</div>
                </div>
                <div>
                    <div style="font-size: 12px; color: var(--text-muted);">Annual Income</div>
                    <div style="font-size: 16px; font-weight: 800; color: var(--text-primary);">₹${income.toLocaleString('en-IN')}</div>
                </div>
            </div>
        </div>

        <h4 style="margin-bottom: 12px; font-size: 1.15rem;">Simulated Eligibility Summary</h4>
        <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: var(--surface-color); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-circle-check" style="color: var(--emerald-accent);"></i>
                    <span style="font-weight: 600; font-size: 14px;">Merit Based Criteria (&ge; 60%)</span>
                </div>
                <span class="status-pill ${marks >= 60 ? 'status-approved' : 'status-rejected'}">
                    ${marks >= 60 ? 'Eligible' : 'Below Cutoff'}
                </span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: var(--surface-color); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-circle-check" style="color: var(--emerald-accent);"></i>
                    <span style="font-weight: 600; font-size: 14px;">Need Based Income Tier (&le; 2.5L)</span>
                </div>
                <span class="status-pill ${income <= 250000 ? 'status-approved' : 'status-under-review'}">
                    ${income <= 250000 ? 'Eligible' : 'Higher Bracket'}
                </span>
            </div>
        </div>

        <div style="display: flex; gap: 12px;">
            <a href="/scholarships.html" class="btn btn-primary" style="flex: 2;">
                <i class="fas fa-magnifying-glass"></i> View Matching Scholarships
            </a>
            <button class="btn btn-outline" onclick="closeEligibilityModal()" style="flex: 1;">Close</button>
        </div>
    `;

    if (window.openModalById) {
        window.openModalById('eligibilityModal');
    } else {
        modal.classList.add('active');
    }
}

function closeEligibilityModal() {
    if (window.closeModalById) {
        window.closeModalById('eligibilityModal');
    } else {
        document.getElementById('eligibilityModal')?.classList.remove('active');
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const isAuth = await checkAuth();
    if (isAuth) {
        loadDashboardData();
    }

    const modal = document.getElementById('eligibilityModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.id === 'eligibilityModal') closeEligibilityModal();
        });
    }
});
