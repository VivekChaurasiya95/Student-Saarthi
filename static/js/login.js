// Student Saarthi - Executive Authentication Engine
var API_URL = window.API_URL || (window.location.origin + '/api');

const studentLoginBtn = document.getElementById('studentLoginBtn');
const adminLoginBtn = document.getElementById('adminLoginBtn');
const studentLoginForm = document.getElementById('studentLoginForm');
const adminLoginForm = document.getElementById('adminLoginForm');
const googleContainer = document.getElementById('googleSignInContainer');

function showStudentLogin() {
    if (studentLoginBtn && adminLoginBtn) {
        studentLoginBtn.className = 'btn btn-primary';
        adminLoginBtn.className = 'btn btn-ghost';
    }
    if (studentLoginForm) studentLoginForm.style.display = 'block';
    if (adminLoginForm) adminLoginForm.style.display = 'none';
    if (googleContainer) googleContainer.style.display = 'block';
    hideMessages();
}

function showAdminLogin() {
    if (adminLoginBtn && studentLoginBtn) {
        adminLoginBtn.className = 'btn btn-primary';
        studentLoginBtn.className = 'btn btn-ghost';
    }
    if (adminLoginForm) adminLoginForm.style.display = 'block';
    if (studentLoginForm) studentLoginForm.style.display = 'none';
    if (googleContainer) googleContainer.style.display = 'none';
    hideMessages();
}

document.addEventListener('DOMContentLoaded', () => {
    // Check URL parameters for admin shortcut
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin') === 'true') {
        showAdminLogin();
    } else {
        showStudentLogin();
    }

    if (studentLoginBtn) studentLoginBtn.addEventListener('click', showStudentLogin);
    if (adminLoginBtn) adminLoginBtn.addEventListener('click', showAdminLogin);

    // Student Login Submission
    if (studentLoginForm) {
        studentLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessages();

            const email = document.getElementById('studentEmail').value.trim();
            const password = document.getElementById('studentPassword').value;

            const submitBtn = studentLoginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Authenticating...';

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                if (response.ok && data.success) {
                    showSuccess('Welcome back! Directing to scholar dashboard...');
                    window.showToast('Authentication successful', 'success');
                    setTimeout(() => {
                        window.location.href = '/student-dashboard.html';
                    }, 800);
                } else {
                    showError(data.error || 'Invalid credentials provided.');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-arrow-right-to-bracket"></i> Sign In As Scholar';
                }
            } catch (err) {
                console.error('Login network error:', err);
                showError('Authentication service unreachable. Please retry.');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-arrow-right-to-bracket"></i> Sign In As Scholar';
            }
        });
    }

    // Admin Login Submission
    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessages();

            const username = document.getElementById('adminUsername').value.trim();
            const password = document.getElementById('adminPassword').value;

            const submitBtn = adminLoginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Verifying Credentials...';

            try {
                const response = await fetch(`${API_URL}/admin/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();
                if (response.ok && data.success) {
                    showSuccess('Master access granted! Initializing command center...');
                    window.showToast('Administrator authenticated', 'success');
                    setTimeout(() => {
                        window.location.href = '/admin-dashboard.html';
                    }, 800);
                } else {
                    showError(data.error || 'Unauthorized administrator access.');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-shield-halved"></i> Authenticate Administrator';
                }
            } catch (err) {
                console.error('Admin login error:', err);
                showError('Authentication gateway error.');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-shield-halved"></i> Authenticate Administrator';
            }
        });
    }
});

// Google Sign-In Callback
function handleGoogleSignIn(response) {
    if (!response || !response.credential) return;

    try {
        const payload = parseJwt(response.credential);
        fetch(`${API_URL}/auth/google`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                token: response.credential,
                email: payload.email,
                name: payload.name,
                google_id: payload.sub
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.showToast('Google authentication successful', 'success');
                showSuccess('Google authentication successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/student-dashboard.html';
                }, 800);
            } else {
                showError(data.error || 'Google Sign-In failed.');
            }
        })
        .catch(err => {
            console.error('Google Auth backend error:', err);
            showError('Failed to communicate with Google auth endpoint.');
        });
    } catch (e) {
        console.error('JWT Decode error:', e);
        showError('Invalid Google credential token.');
    }
}

function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
}

function showError(msg) {
    const el = document.getElementById('errorMessage');
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
    }
}

function showSuccess(msg) {
    const el = document.getElementById('successMessage');
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
    }
}

function hideMessages() {
    const err = document.getElementById('errorMessage');
    const succ = document.getElementById('successMessage');
    if (err) err.style.display = 'none';
    if (succ) succ.style.display = 'none';
}

// Google Sign-In Ad-Blocker Fallback Handler
window.handleGoogleGsiBlocked = function() {
    const notice = document.getElementById('googleBlockedNotice');
    if (notice) notice.style.display = 'block';
};

window.addEventListener('load', () => {
    setTimeout(() => {
        const gsiBtn = document.querySelector('.g_id_signin');
        if (gsiBtn && gsiBtn.children.length === 0) {
            window.handleGoogleGsiBlocked();
        }
    }, 1500);
});
