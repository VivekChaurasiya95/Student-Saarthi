import json

def test_registration_success(client):
    """Test successful student registration."""
    payload = {
        'fullName': 'Aarav Patel',
        'email': 'aarav.patel@example.com',
        'password': 'SecurePassword123',
        'phone': '9812345678',
        'dob': '2004-05-15',
        'gender': 'Male',
        'educationLevel': 'Undergraduate',
        'academicPercentage': 88.5,
        'fieldOfStudy': 'Computer Science',
        'institutionName': 'ABC Institute of Tech',
        'graduationYear': 2026,
        'category': 'General',
        'annualIncome': 350000
    }
    response = client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert 'userId' in data

def test_registration_duplicate_email(client):
    """Test rejection of duplicate email registration."""
    payload = {
        'fullName': 'User One',
        'email': 'duplicate@example.com',
        'password': 'Password123'
    }
    # Register once
    res1 = client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    assert res1.status_code == 201

    # Attempt duplicate
    res2 = client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    assert res2.status_code == 400
    assert 'already registered' in res2.get_json()['error'].lower()

def test_registration_validation_errors(client):
    """Test invalid registration payloads."""
    # Missing email
    res = client.post('/api/register', data=json.dumps({'fullName': 'No Email', 'password': '123'}), content_type='application/json')
    assert res.status_code == 400

    # Short password
    res = client.post('/api/register', data=json.dumps({'fullName': 'Short Pass', 'email': 'valid@test.com', 'password': '123'}), content_type='application/json')
    assert res.status_code == 400

def test_student_login_success(client):
    """Test student login with valid credentials."""
    # Register
    client.post('/api/register', data=json.dumps({
        'fullName': 'Login Tester',
        'email': 'logintester@example.com',
        'password': 'MyPassword123'
    }), content_type='application/json')

    # Login
    response = client.post('/api/login', data=json.dumps({
        'email': 'logintester@example.com',
        'password': 'MyPassword123'
    }), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['userName'] == 'Login Tester'

def test_student_login_invalid(client):
    """Test student login with incorrect password."""
    response = client.post('/api/login', data=json.dumps({
        'email': 'nobody@example.com',
        'password': 'WrongPassword'
    }), content_type='application/json')
    assert response.status_code == 401

def test_admin_login(client):
    """Test administrator authentication."""
    # Success
    res_ok = client.post('/api/admin/login', data=json.dumps({
        'username': 'admin',
        'password': 'admin123'
    }), content_type='application/json')
    assert res_ok.status_code == 200
    assert res_ok.get_json()['success'] is True

    # Failure
    res_fail = client.post('/api/admin/login', data=json.dumps({
        'username': 'admin',
        'password': 'wrongpassword'
    }), content_type='application/json')
    assert res_fail.status_code == 401

def test_logout(student_auth_client):
    """Test session clearing on logout."""
    res = student_auth_client.post('/api/logout')
    assert res.status_code == 200
    
    # Check session should now report loggedIn: False
    sess_res = student_auth_client.get('/api/check-session')
    assert sess_res.get_json()['loggedIn'] is False

