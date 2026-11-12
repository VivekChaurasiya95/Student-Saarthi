// Student Saarthi - Executive Homepage Interactions
var API_URL = window.API_URL || (window.location.origin + '/api');

// Animate numeric statistics counters smoothly
function animateCounter(elementId, target) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let current = 0;
    const duration = 1200;
    const steps = 40;
    const stepTime = Math.floor(duration / steps);
    const increment = Math.max(1, Math.floor(target / steps));
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString('en-IN') + '+';
            clearInterval(timer);
        } else {
            element.textContent = current.toLocaleString('en-IN');
        }
    }, stepTime);
}

// Load statistics telemetry from backend
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        if (response.ok) {
            const data = await response.json();
            animateCounter('totalScholarships', data.scholarships || 10);
            animateCounter('totalStudents', data.students || 0);
            const rateEl = document.getElementById('successRate');
            if (rateEl) {
                rateEl.textContent = (data.successRate || 100) + '%';
            }
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        const schEl = document.getElementById('totalScholarships');
        const stuEl = document.getElementById('totalStudents');
        const rateEl = document.getElementById('successRate');
        if (schEl) schEl.textContent = '10+';
        if (stuEl) stuEl.textContent = '0+';
        if (rateEl) rateEl.textContent = '100%';
    }
}

// Determine scholarship badge style based on category
function getCategoryBadgeClass(category) {
    const cat = (category || '').toLowerCase();
    if (cat.includes('merit') || cat.includes('academic')) return 'badge-academic';
    if (cat.includes('need') || cat.includes('income') || cat.includes('means')) return 'badge-need';
    if (cat.includes('women') || cat.includes('girl')) return 'badge-women';
    return 'badge-general';
}

// Render a single luxury bento scholarship card
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
    const amountFormatted = amountVal > 0 ? `₹${amountVal.toLocaleString('en-IN')}` : 'Full Funding';
    const firstLevel = scholarship.education_levels ? scholarship.education_levels.split(',')[0].trim() : 'Higher Ed';
    const badgeClass = getCategoryBadgeClass(scholarship.category);
    
    return `
        <div class="scholarship-card">
            <div class="scholarship-header">
                <div>
                    <div class="scholarship-amount-tag">${amountFormatted}</div>
                    <div class="scholarship-amount-sub">Grant Allowance</div>
                </div>
                <span class="scholarship-badge ${badgeClass}">${scholarship.category || 'General'}</span>
            </div>
            
            <div class="scholarship-body">
                <h3>${scholarship.name}</h3>
                <p class="scholarship-provider">
                    <i class="fas fa-building-columns"></i>
                    ${scholarship.provider || 'Government of India'}
                </p>
                <p class="scholarship-description">${scholarship.description || 'Verified financial support program for qualified scholars meeting criteria.'}</p>
                
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
                        <i class="fas fa-location-dot"></i>
                        ${scholarship.state || 'All States'}
                    </span>
                </div>
            </div>
            
            <div class="scholarship-footer">
                <span class="deadline-chip ${isUrgent ? 'urgent' : ''}">
                    <i class="fas ${isUrgent ? 'fa-triangle-exclamation' : 'fa-clock'}"></i>
                    ${daysLeftText}
                </span>
                <a href="/scholarship_detail.html?id=${scholarship.id}" class="btn btn-primary btn-sm">
                    View Details
                    <i class="fas fa-chevron-right" style="font-size: 11px;"></i>
                </a>
            </div>
        </div>
    `;
}

// Load Featured Scholarships
async function loadFeaturedScholarships() {
    const container = document.getElementById('featuredScholarships');
    if (!container) return;

    try {
        const response = await fetch(`${API_URL}/scholarships/featured`);
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        
        const scholarships = await response.json();
        if (!scholarships || scholarships.length === 0) {
            container.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 48px;">
                    <i class="fas fa-box-open" style="font-size: 44px; color: var(--text-muted); margin-bottom: 16px;"></i>
                    <h3 style="margin-bottom: 6px;">No Featured Scholarships Available</h3>
                    <p style="color: var(--text-secondary);">Check back shortly as new government grants are being verified.</p>
                </div>
            `;
            return;
        }
        container.innerHTML = scholarships.map(sch => createScholarshipCard(sch)).join('');
    } catch (error) {
        console.error('Error loading featured scholarships:', error);
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 48px;">
                <i class="fas fa-circle-exclamation" style="font-size: 44px; color: var(--error-color); margin-bottom: 16px;"></i>
                <h3 style="margin-bottom: 6px;">Unable To Load Scholarships</h3>
                <p style="color: var(--text-secondary);">Please verify backend connectivity or refresh the page.</p>
            </div>
        `;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadFeaturedScholarships();
});
