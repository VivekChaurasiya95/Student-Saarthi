// Student Saarthi - Student Registration JavaScript
var API_URL = window.API_URL || (window.location.origin + '/api');

const signupForm = document.getElementById('signupForm');

// Real-time Field Validation
function validateEmail() {
    const email = document.getElementById('email');
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(email.value.trim())) {
        showFieldError(email, 'Please enter a valid email address');
        return false;
    }
    clearFieldError(email);
    return true;
}

function validatePhone() {
    const phone = document.getElementById('phone');
    const regex = /^[0-9]{10}$/;
    if (!regex.test(phone.value.trim())) {
        showFieldError(phone, 'Please enter a valid 10-digit mobile number');
        return false;
    }
    clearFieldError(phone);
    return true;
}

function validatePassword() {
    const password = document.getElementById('password');
    if (password.value.length < 6) {
        showFieldError(password, 'Password must be at least 6 characters long');
        return false;
    }
    clearFieldError(password);
    validateConfirmPassword();
    return true;
}

function validateConfirmPassword() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    if (confirmPassword.value && password.value !== confirmPassword.value) {
        showFieldError(confirmPassword, 'Passwords do not match');
        return false;
    }
    clearFieldError(confirmPassword);
    return true;
}

function validatePercentage() {
    const percentage = document.getElementById('academicPercentage');
    const value = parseFloat(percentage.value);
    if (isNaN(value) || value < 40 || value > 100) {
        showFieldError(percentage, 'Percentage must be between 40 and 100');
        return false;
    }
    clearFieldError(percentage);
    return true;
}

function showFieldError(field, msg) {
    clearFieldError(field);
    const errDiv = document.createElement('div');
    errDiv.className = 'field-error-message';
    errDiv.style.color = 'var(--error-color)';
    errDiv.style.fontSize = '12px';
    errDiv.style.marginTop = '4px';
    errDiv.textContent = msg;
    field.parentNode.appendChild(errDiv);
    field.style.borderColor = 'var(--error-color)';
}

function clearFieldError(field) {
    const existing = field.parentNode.querySelector('.field-error-message');
    if (existing) existing.remove();
    field.style.borderColor = '';
}

document.addEventListener('DOMContentLoaded', () => {
    const emailField = document.getElementById('email');
    const phoneField = document.getElementById('phone');
    const passField = document.getElementById('password');
    const confField = document.getElementById('confirmPassword');
    const pctField = document.getElementById('academicPercentage');

    if (emailField) emailField.addEventListener('blur', validateEmail);
    if (phoneField) phoneField.addEventListener('blur', validatePhone);
    if (passField) passField.addEventListener('input', validatePassword);
    if (confField) confField.addEventListener('input', validateConfirmPassword);
    if (pctField) pctField.addEventListener('blur', validatePercentage);

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessages();

            const isEmailOk = validateEmail();
            const isPhoneOk = validatePhone();
            const isPassOk = validatePassword();
            const isConfOk = validateConfirmPassword();
            const isPctOk = validatePercentage();

            if (!isEmailOk || !isPhoneOk || !isPassOk || !isConfOk || !isPctOk) {
                showError('Please correct the validation errors in the form.');
                return;
            }

            if (!document.getElementById('agreeTerms').checked) {
                showError('You must agree to the Terms of Service and Privacy Policy to register.');
                return;
            }

            const payload = {
                fullName: document.getElementById('fullName').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                password: document.getElementById('password').value,
                dob: document.getElementById('dob').value,
                gender: document.getElementById('gender').value,
                address: document.getElementById('address')?.value.trim() || '',
                educationLevel: document.getElementById('educationLevel').value,
                academicPercentage: parseFloat(document.getElementById('academicPercentage').value),
                fieldOfStudy: document.getElementById('fieldOfStudy').value.trim(),
                institutionName: document.getElementById('institutionName').value.trim(),
                graduationYear: parseInt(document.getElementById('graduationYear').value),
                category: document.getElementById('category').value,
                annualIncome: parseInt(document.getElementById('annualIncome').value),
                specialCircumstances: document.getElementById('specialCircumstances')?.value.trim() || ''
            };

            const submitBtn = signupForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span> Creating your profile...';

            try {
                const response = await fetch(`${API_URL}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                if (response.ok && data.success) {
                    showSuccess('Account created successfully! Preparing your dashboard...');
                    setTimeout(() => {
                        window.location.href = '/student-dashboard.html';
                    }, 1200);
                } else {
                    showError(data.error || 'Registration failed. Please try again.');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-user-plus"></i> Create Account';
                }
            } catch (err) {
                console.error('Registration error:', err);
                showError('Connection error. Please ensure the backend server is running.');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-user-plus"></i> Create Account';
            }
        });
    }
});

function showError(msg) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.textContent = msg;
        errorDiv.style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function showSuccess(msg) {
    const successDiv = document.getElementById('successMessage');
    if (successDiv) {
        successDiv.textContent = msg;
        successDiv.style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function hideMessages() {
    const err = document.getElementById('errorMessage');
    const succ = document.getElementById('successMessage');
    if (err) err.style.display = 'none';
    if (succ) succ.style.display = 'none';
}

