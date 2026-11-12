import json

def test_public_pages_render(client):
    """Test that all public frontend pages render without errors."""
    pages = [
        '/',
        '/index.html',
        '/about.html',
        '/contact.html',
        '/helpCentre.html',
        '/PrivacyPolicy.html',
        '/termOfServices.html',
        '/scholarships.html',
        '/developers.html',
        '/developers',
        '/login.html',
        '/signup.html'
    ]
    for page in pages:
        response = client.get(page)
        assert response.status_code == 200, f"Page {page} failed with status {response.status_code}"
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data

def test_static_assets_serve(client):
    """Verify that CSS and JavaScript static assets are accessible."""
    # CSS
    css_res = client.get('/static/css/styles.css')
    assert css_res.status_code == 200
    assert b':root' in css_res.data or b'body' in css_res.data

    # JS
    js_res = client.get('/static/js/index.js')
    assert js_res.status_code == 200
    assert b'API_URL' in js_res.data

def test_health_check_endpoint(client):
    """Verify system health endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'database' in data

def test_stats_endpoint(client):
    """Verify portal statistics calculation."""
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'scholarships' in data
    assert 'students' in data
    assert 'totalApplications' in data

def test_contact_submission(client):
    """Test contact message dispatch."""
    payload = {
        'name': 'Pooja Verma',
        'email': 'pooja.verma@example.com',
        'subject': 'Scholarship Query',
        'message': 'Hello, I wanted to verify the deadline for the technical degree scholarship.'
    }
    response = client.post('/api/contact', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    assert response.get_json()['success'] is True

def test_developers_page(client):
    """Verify developers engineering team page contents."""
    response = client.get('/developers.html')
    assert response.status_code == 200
    assert b'Core Engineering Contributors' in response.data
    assert b'Vivek Chaurasiya' in response.data
    assert b'Prajwal Patidar' in response.data
    assert b'Atul Dehariya' in response.data
    assert b'https://github.com/VivekChaurasiya95/Student-Saarthi' in response.data


