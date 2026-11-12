import json

def test_unauthenticated_apply(client):
    """Anonymous users cannot apply for scholarships."""
    response = client.post('/api/apply', data=json.dumps({
        'scholarshipId': 1,
        'sop': 'This is a valid statement of purpose describing my academic goals.'
    }), content_type='application/json')
    assert response.status_code == 401

def test_apply_success(student_auth_client):
    """Test successful application submission by student."""
    payload = {
        'scholarshipId': 1,
        'sop': 'This is my comprehensive statement of purpose exceeding fifty characters requirement for application.',
        'achievements': 'State rank 15 in science olympiad',
        'extracurricular': 'School debate team captain'
    }
    response = student_auth_client.post('/api/apply', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert 'applicationId' in data

def test_apply_duplicate_rejected(student_auth_client):
    """Prevent duplicate applications to the same scholarship."""
    payload = {
        'scholarshipId': 1,
        'sop': 'First submission statement of purpose meeting required character length.'
    }
    # First submit
    student_auth_client.post('/api/apply', data=json.dumps(payload), content_type='application/json')

    # Second submit
    res = student_auth_client.post('/api/apply', data=json.dumps(payload), content_type='application/json')
    assert res.status_code == 400
    assert 'already applied' in res.get_json()['error'].lower()

def test_get_applications(student_auth_client):
    """Test retrieving student's applications list."""
    res = student_auth_client.get('/api/applications')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)

def test_student_bookmarks_workflow(student_auth_client):
    """Test bookmarking and un-bookmarking scholarships."""
    # Add bookmark
    add_res = student_auth_client.post('/api/bookmarks', data=json.dumps({'scholarshipId': 1}), content_type='application/json')
    assert add_res.status_code == 201

    # Get bookmarks
    get_res = student_auth_client.get('/api/bookmarks')
    assert get_res.status_code == 200
    bookmarks = get_res.get_json()
    assert len(bookmarks) == 1
    assert bookmarks[0]['id'] == 1

    # Remove bookmark
    del_res = student_auth_client.delete('/api/bookmarks/1')
    assert del_res.status_code == 200

    # Verify removal
    get_res2 = student_auth_client.get('/api/bookmarks')
    assert len(get_res2.get_json()) == 0

