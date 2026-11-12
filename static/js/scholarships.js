// Student Saarthi - Executive Scholarships Discovery Engine
var API_URL = window.API_URL || (window.location.origin + '/api');

let allScholarships = [];
let currentUser = null;
let currentView = 'grid'; // 'grid' | 'list'
let userBookmarks = new Set();

// Check user session (Reuses singleton promise from navbar if present)
async function checkSession() {
    try {
        const data = window.getAppSession 
            ? await window.getAppSession() 
            : await (await fetch(`${API_URL}/check-session`, { credentials: 'include' })).json();
        if (data && data.loggedIn && data.type === 'user') {
            currentUser = data;
            loadUserBookmarks();
        }
    } catch (error) {
        console.warn('Session check warning:', error);
    }
}

// Load current user bookmarks
async function loadUserBookmarks() {
    try {
        const response = await fetch(`${API_URL}/bookmarks`, { credentials: 'include' });
        if (response.ok) {
            const list = await response.json();
            if (Array.isArray(list)) {
                userBookmarks = new Set(list.map(b => b.scholarship_id || b.id));
                // Re-render if scholarships are already loaded
                if (allScholarships.length > 0) {
                    applyFilters();
                }
            }
        }
    } catch (e) {
        console.warn('Bookmarks load error:', e);
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

// Load all scholarships from backend
async function loadScholarships() {
    const container = document.getElementById('scholarshipsContainer');
    const resultsCount = document.getElementById('resultsCount');

    try {
        const response = await fetch(`${API_URL}/scholarships`, { credentials: 'include' });
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        
        allScholarships = await response.json();
        displayScholarships(allScholarships);
    } catch (error) {
        console.error('Error loading scholarships:', error);
        if (container) {
            container.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
                    <i class="fas fa-circle-exclamation" style="font-size: 48px; color: var(--error-color); margin-bottom: 16px;"></i>
                    <h3 style="margin-bottom: 8px;">Failed To Load Catalog</h3>
                    <p style="color: var(--text-secondary); max-width: 450px; margin: 0 auto 20px;">${error.message}</p>
                    <button class="btn btn-outline" onclick="loadScholarships()">
                        <i class="fas fa-rotate"></i> Retry Connection
                    </button>
                </div>
            `;
        }
        if (resultsCount) {
            resultsCount.className = 'status-pill status-rejected';
            resultsCount.innerHTML = '<i class="fas fa-circle-xmark"></i> Connection Error';
        }
    }
}

// Display scholarships list/grid
function displayScholarships(scholarships) {
    const container = document.getElementById('scholarshipsContainer');
    const resultsCount = document.getElementById('resultsCount');

    if (!container) return;

    if (resultsCount) {
        resultsCount.className = 'status-pill status-submitted';
        resultsCount.innerHTML = `<i class="fas fa-layer-group"></i> Showing ${scholarships.length} Verified Grant${scholarships.length !== 1 ? 's' : ''}`;
    }

    if (scholarships.length === 0) {
        container.className = 'scholarships-grid';
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 70px 20px;">
                <div class="feature-icon-box" style="margin: 0 auto 20px; width: 64px; height: 64px; font-size: 26px;">
                    <i class="fas fa-filter-circle-xmark"></i>
                </div>
                <h3 style="margin-bottom: 8px;">No Matching Scholarships Found</h3>
                <p style="color: var(--text-secondary); max-width: 480px; margin: 0 auto 24px;">
                    No grants match your current criteria. Try expanding your education level, reducing the minimum percentage filter, or clearing search keywords.
                </p>
                <button class="btn btn-primary" onclick="resetAllFilters()">
                    <i class="fas fa-rotate-left"></i> Reset All Filters
                </button>
            </div>
        `;
        return;
    }

    container.className = currentView === 'list' ? 'scholarships-list' : 'scholarships-grid';
    container.innerHTML = scholarships.map(sch => createScholarshipCard(sch)).join('');
}

// Generate luxury bento card HTML
function createScholarshipCard(scholarship) {
    const deadline = scholarship.deadline ? new Date(scholarship.deadline) : null;
    const today = new Date();
    let daysLeftText = 'Open Application';
    let isUrgent = false;

    if (deadline && !isNaN(deadline.getTime())) {
        const diffTime = deadline - today;
        const daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        if (daysLeft > 0) {
            daysLeftText = `${daysLeft} days left`;
            isUrgent = daysLeft <= 25;
        } else {
            daysLeftText = 'Closed';
        }
    }

    const amountVal = parseFloat(scholarship.amount || 0);
    const amountFormatted = amountVal > 0 ? `₹${amountVal.toLocaleString('en-IN')}` : 'Full Grant';
    const firstLevel = scholarship.education_levels ? scholarship.education_levels.split(',')[0].trim() : 'Higher Ed';
    const badgeClass = getCategoryBadgeClass(scholarship.category);
    const isBookmarked = userBookmarks.has(scholarship.id);

    return `
        <div class="scholarship-card">
            <div class="scholarship-header">
                <div>
                    <div class="scholarship-amount-tag">${amountFormatted}</div>
                    <div class="scholarship-amount-sub">Annual Allowance</div>
                </div>
                <span class="scholarship-badge ${badgeClass}">${scholarship.category || 'General'}</span>
            </div>
            
            <div class="scholarship-body">
                <h3>${scholarship.name}</h3>
                <p class="scholarship-provider">
                    <i class="fas fa-building-columns"></i>
                    ${scholarship.provider || 'Government of India'}
                </p>
                <p class="scholarship-description">${scholarship.description || 'Verified educational aid program for eligible scholars.'}</p>
                
                <div class="scholarship-meta-pills">
                    <span class="meta-pill">
                        <i class="fas fa-graduation-cap"></i>
                        ${firstLevel}
                    </span>
                    <span class="meta-pill">
                        <i class="fas fa-percent"></i>
                        ${scholarship.min_percentage ? scholarship.min_percentage + '% min' : 'Merit Based'}
                    </span>
                    <span class="meta-pill">
                        <i class="fas fa-users"></i>
                        ${scholarship.current_applicants || 0} enrolled
                    </span>
                </div>
            </div>
            
            <div class="scholarship-footer">
                <span class="deadline-chip ${isUrgent ? 'urgent' : ''}">
                    <i class="fas ${isUrgent ? 'fa-triangle-exclamation' : 'fa-clock'}"></i>
                    ${daysLeftText}
                </span>
                
                <div style="display: flex; align-items: center; gap: 8px;">
                    ${currentUser ? `
                        <button class="btn-bookmark ${isBookmarked ? 'bookmarked' : ''}" 
                                onclick="toggleBookmark(${scholarship.id}, this)" 
                                title="${isBookmarked ? 'Saved to Wishlist' : 'Bookmark Scholarship'}">
                            <i class="fa${isBookmarked ? 's' : 'r'} fa-bookmark"></i>
                        </button>
                    ` : ''}
                    <button class="btn btn-primary btn-sm" onclick="viewScholarshipDetails(${scholarship.id})">
                        Details <i class="fas fa-chevron-right" style="font-size: 11px;"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Multi-Criteria Dynamic Filter
function applyFilters() {
    const searchTerm = (document.getElementById('searchInput')?.value || '').toLowerCase();
    const category = document.getElementById('categoryFilter')?.value || '';
    const amountRange = document.getElementById('amountFilter')?.value || '';
    const education = document.getElementById('educationFilter')?.value || '';
    const deadline = document.getElementById('deadlineFilter')?.value || '';

    const filtered = allScholarships.filter(s => {
        // Keyword Search
        if (searchTerm) {
            const nameMatch = (s.name || '').toLowerCase().includes(searchTerm);
            const descMatch = (s.description || '').toLowerCase().includes(searchTerm);
            const provMatch = (s.provider || '').toLowerCase().includes(searchTerm);
            const catMatch = (s.category || '').toLowerCase().includes(searchTerm);
            if (!nameMatch && !descMatch && !provMatch && !catMatch) return false;
        }

        // Category Filter
        if (category && !(s.category || '').toLowerCase().includes(category.toLowerCase())) {
            return false;
        }

        // Amount Filter
        if (amountRange) {
            const [min, max] = amountRange.split('-').map(Number);
            const amt = parseFloat(s.amount || 0);
            if (amt < min || amt > max) return false;
        }

        // Education Level Filter
        if (education && s.education_levels) {
            if (!s.education_levels.toLowerCase().includes(education.toLowerCase())) {
                return false;
            }
        }

        // Deadline Filter
        if (deadline && s.deadline) {
            const daysLeft = Math.ceil((new Date(s.deadline) - new Date()) / (1000 * 60 * 60 * 24));
            if (daysLeft > parseInt(deadline) || daysLeft < 0) return false;
        }

        return true;
    });

    displayScholarships(filtered);
}

// Reset all filters to default
function resetAllFilters() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const amountFilter = document.getElementById('amountFilter');
    const educationFilter = document.getElementById('educationFilter');
    const deadlineFilter = document.getElementById('deadlineFilter');

    if (searchInput) searchInput.value = '';
    if (categoryFilter) categoryFilter.value = '';
    if (amountFilter) amountFilter.value = '';
    if (educationFilter) educationFilter.value = '';
    if (deadlineFilter) deadlineFilter.value = '';

    // Reset Category Chips
    document.querySelectorAll('#categoryChips .chip-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-category') === '');
    });

    displayScholarships(allScholarships);
}

// Modern Modal View Details
async function viewScholarshipDetails(scholarshipId) {
    try {
        const response = await fetch(`${API_URL}/scholarships/${scholarshipId}`);
        if (!response.ok) throw new Error('Scholarship details could not be retrieved');
        
        const scholarship = await response.json();
        const deadline = scholarship.deadline ? new Date(scholarship.deadline) : null;
        let daysLeftText = 'Open Rolling';
        let daysLeft = 999;
        
        if (deadline && !isNaN(deadline.getTime())) {
            daysLeft = Math.ceil((deadline - new Date()) / (1000 * 60 * 60 * 24));
            daysLeftText = `${deadline.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })} (${daysLeft > 0 ? `${daysLeft} days left` : 'Expired'})`;
        }

        const modalBody = document.getElementById('modalBody');
        const modalTitle = document.getElementById('modalScholarshipTitle');
        if (modalTitle) modalTitle.textContent = scholarship.name;

        const docsList = scholarship.required_documents 
            ? scholarship.required_documents.split(',').map(d => `<li style="padding: 4px 0;"><i class="fas fa-circle-check" style="color: var(--emerald-accent); margin-right: 8px;"></i>${d.trim()}</li>`).join('')
            : '<li style="padding: 4px 0;"><i class="fas fa-circle-check" style="color: var(--emerald-accent); margin-right: 8px;"></i>Standard academic and income proof documents</li>';
        
        const badgeClass = getCategoryBadgeClass(scholarship.category);
        const amountVal = parseFloat(scholarship.amount || 0);

        modalBody.innerHTML = `
            <div style="margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 16px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                            <span class="scholarship-badge ${badgeClass}">${scholarship.category}</span>
                            ${scholarship.is_verified ? '<span class="status-pill status-approved"><i class="fas fa-shield-check"></i> Gazette Verified</span>' : ''}
                        </div>
                        <p style="color: var(--text-secondary); display: flex; align-items: center; gap: 8px; font-size: 15px; margin: 0;">
                            <i class="fas fa-building-columns" style="color: var(--brand-blue);"></i>
                            <strong>${scholarship.provider}</strong>
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 2rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.02em;">
                            ₹${amountVal.toLocaleString('en-IN')}
                        </div>
                        <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; text-transform: uppercase;">Direct Grant Amount</div>
                    </div>
                </div>

                <!-- Stats Overview Bar -->
                <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 28px;">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 16px;">
                        <div>
                            <span style="color: var(--text-muted); font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Deadline Date</span>
                            <p style="font-size: 14.5px; margin-top: 4px; font-weight: 700; color: ${daysLeft <= 25 ? 'var(--error-color)' : 'var(--text-primary)'};">
                                ${daysLeftText}
                            </p>
                        </div>
                        <div>
                            <span style="color: var(--text-muted); font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Min Academic Score</span>
                            <p style="font-size: 14.5px; margin-top: 4px; font-weight: 700; color: var(--text-primary);">${scholarship.min_percentage || 0}% Aggregate</p>
                        </div>
                        <div>
                            <span style="color: var(--text-muted); font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Candidate Intake</span>
                            <p style="font-size: 14.5px; margin-top: 4px; font-weight: 700; color: var(--text-primary);">${scholarship.current_applicants || 0} ${scholarship.max_applicants ? `/ ${scholarship.max_applicants}` : 'applied'}</p>
                        </div>
                    </div>
                </div>

                <h4 style="margin-bottom: 10px; font-size: 1.15rem;">Program Description</h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: 24px; font-size: 14.5px;">
                    ${scholarship.description || 'Comprehensive financial aid program initiated to support ambitious and high-achieving scholars.'}
                </p>

                <h4 style="margin-bottom: 10px; font-size: 1.15rem;">Eligibility Criteria</h4>
                <ul style="color: var(--text-secondary); line-height: 1.9; margin-bottom: 24px; list-style: none; padding-left: 0;">
                    <li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Academic Requirement: Minimum <strong>${scholarship.min_percentage || 0}%</strong> marks in previous examination.</li>
                    <li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Permitted Levels: <strong>${scholarship.education_levels || 'All eligible education levels'}</strong></li>
                    <li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Reservation Category: <strong>${scholarship.eligible_categories || 'Open to all categories'}</strong></li>
                    ${scholarship.max_income ? `<li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Income Ceiling: Annual family income under <strong>₹${parseFloat(scholarship.max_income).toLocaleString('en-IN')}</strong></li>` : ''}
                    ${scholarship.age_limit ? `<li><i class="fas fa-check" style="color: var(--brand-blue); margin-right: 8px;"></i>Age Cap: Must be under <strong>${scholarship.age_limit} years</strong></li>` : ''}
                </ul>

                <h4 style="margin-bottom: 10px; font-size: 1.15rem;">Required Verification Documents</h4>
                <ul style="color: var(--text-secondary); line-height: 1.9; margin-bottom: 24px; list-style: none; padding-left: 0;">
                    ${docsList}
                </ul>

                ${scholarship.official_url ? `
                    <div style="background: rgba(37, 99, 235, 0.06); border: 1px solid rgba(37, 99, 235, 0.2); padding: 14px 18px; border-radius: var(--radius-md); margin-bottom: 28px;">
                        <p style="font-size: 13.5px; color: var(--text-primary); margin: 0;">
                            <i class="fas fa-arrow-up-right-from-square" style="color: var(--brand-blue); margin-right: 8px;"></i>
                            Gazette Reference: <a href="${scholarship.official_url}" target="_blank" rel="noopener noreferrer" style="color: var(--brand-blue); font-weight: 600;">${scholarship.official_source || 'Official Department Portal'}</a>
                        </p>
                    </div>
                ` : ''}

                <!-- Modal Actions -->
                <div style="display: flex; gap: 14px; margin-top: 28px;">
                    ${currentUser ? `
                        <a href="/apply?id=${scholarship.id}" class="btn btn-primary" style="flex: 2;">
                            <i class="fas fa-paper-plane"></i> Proceed To Application
                        </a>
                        <button class="btn btn-outline" onclick="toggleBookmark(${scholarship.id}, this)" style="flex: 1;">
                            <i class="fas fa-bookmark"></i> Wishlist
                        </button>
                    ` : `
                        <a href="/login.html" class="btn btn-primary" style="flex: 1;">
                            <i class="fas fa-arrow-right-to-bracket"></i> Login To Submit Application
                        </a>
                    `}
                </div>
            </div>
        `;

        const modal = document.getElementById('scholarshipModal');
        if (modal) modal.classList.add('active');
    } catch (error) {
        console.error('Error fetching scholarship details:', error);
        window.showToast('Failed to load scholarship details', 'error');
    }
}

// Close details modal
function closeModal() {
    const modal = document.getElementById('scholarshipModal');
    if (modal) modal.classList.remove('active');
}

// Toggle Bookmark with Instant Toast Feedback
async function toggleBookmark(scholarshipId, buttonElement) {
    if (!currentUser) {
        window.location.href = '/login.html';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/bookmarks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ scholarshipId })
        });
        
        const data = await response.json();
        if (response.ok) {
            if (userBookmarks.has(scholarshipId)) {
                userBookmarks.delete(scholarshipId);
                window.showToast('Removed from your saved scholarships', 'info');
            } else {
                userBookmarks.add(scholarshipId);
                window.showToast('Scholarship bookmarked to your profile', 'success');
            }
            if (buttonElement) {
                const isBookmarked = userBookmarks.has(scholarshipId);
                buttonElement.classList.toggle('bookmarked', isBookmarked);
                const icon = buttonElement.querySelector('i');
                if (icon) {
                    icon.className = `fa${isBookmarked ? 's' : 'r'} fa-bookmark`;
                }
            }
        } else {
            window.showToast(data.error || 'Failed to update bookmark', 'error');
        }
    } catch (e) {
        window.showToast('Network error while saving bookmark', 'error');
    }
}

// Initialize Discovery Portal
document.addEventListener('DOMContentLoaded', () => {
    checkSession();
    loadScholarships();

    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const amountFilter = document.getElementById('amountFilter');
    const educationFilter = document.getElementById('educationFilter');
    const deadlineFilter = document.getElementById('deadlineFilter');
    const clearFiltersBtn = document.getElementById('clearFilters');

    if (searchInput) searchInput.addEventListener('input', applyFilters);
    if (categoryFilter) categoryFilter.addEventListener('change', () => {
        const selected = categoryFilter.value;
        // Synchronize chip button active state
        document.querySelectorAll('#categoryChips .chip-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-category') === selected);
        });
        applyFilters();
    });
    if (amountFilter) amountFilter.addEventListener('change', applyFilters);
    if (educationFilter) educationFilter.addEventListener('change', applyFilters);
    if (deadlineFilter) deadlineFilter.addEventListener('change', applyFilters);

    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', resetAllFilters);
    }

    // Category Chips Click Handlers
    document.querySelectorAll('#categoryChips .chip-btn').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('#categoryChips .chip-btn').forEach(b => b.classList.remove('active'));
            chip.classList.add('active');
            const cat = chip.getAttribute('data-category');
            if (categoryFilter) categoryFilter.value = cat;
            applyFilters();
        });
    });

    // View Switching (Grid vs List)
    const viewGridBtn = document.getElementById('viewGridBtn');
    const viewListBtn = document.getElementById('viewListBtn');
    if (viewGridBtn && viewListBtn) {
        viewGridBtn.addEventListener('click', () => {
            currentView = 'grid';
            viewGridBtn.className = 'btn btn-sm btn-primary';
            viewListBtn.className = 'btn btn-sm btn-ghost';
            applyFilters();
        });
        viewListBtn.addEventListener('click', () => {
            currentView = 'list';
            viewListBtn.className = 'btn btn-sm btn-primary';
            viewGridBtn.className = 'btn btn-sm btn-ghost';
            applyFilters();
        });
    }

    // Modal Background Click Closes Modal
    const modal = document.getElementById('scholarshipModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.id === 'scholarshipModal') closeModal();
        });
    }

    // Auto-open modal if ID param exists
    const urlParams = new URLSearchParams(window.location.search);
    const scholarshipId = urlParams.get('id');
    if (scholarshipId) {
        setTimeout(() => {
            viewScholarshipDetails(parseInt(scholarshipId));
        }, 350);
    }
});
