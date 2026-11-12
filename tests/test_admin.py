import json

def test_admin_endpoints_require_admin_auth(client, student_auth_client):
    """Ensure non-admins cannot access admin endpoints."""
    # Guest user
    res_guest = client.get('/api/admin/applications')
    assert res_guest.status_code == 401

    # Student user
    res_student = student_auth_client.get('/api/admin/applications')
    assert res_student.status_code == 401

def test_admin_get_applications(admin_auth_client):
    """Admin can fetch all student applications."""
    response = admin_auth_client.get('/api/admin/applications')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_admin_create_and_delete_scholarship(admin_auth_client):
    """Admin can add, modify, and delete scholarships."""
    # 1. Create
    payload = {
        'name': 'CSR STEM Fellowship',
        'provider': 'Tech Corp Foundation',
        'amount': 75000.0,
        'category': 'Academic',
        'description': 'Fellowship for STEM scholars in accredited universities.',
        'minPercentage': 70.0,
        'educationLevels': 'Undergraduate',
        'deadline': '2026-11-30',
        'maxIncome': 800000
    }
    create_res = admin_auth_client.post('/api/admin/scholarships', data=json.dumps(payload), content_type='application/json')
    assert create_res.status_code == 201
    data = create_res.get_json()
    assert data['success'] is True
    sch_id = data['scholarshipId']

    # 2. Update
    update_res = admin_auth_client.put(f'/api/admin/scholarships/{sch_id}', data=json.dumps({
        'amount': 85000.0
    }), content_type='application/json')
    assert update_res.status_code == 200
    assert update_res.get_json()['scholarship']['amount'] == 85000.0

    # 3. Delete
    delete_res = admin_auth_client.delete(f'/api/admin/scholarships/{sch_id}')
    assert delete_res.status_code == 200

def test_admin_get_users(admin_auth_client):
    """Admin can list registered student users."""
    response = admin_auth_client.get('/api/admin/users')
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)

