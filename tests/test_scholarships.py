import json

def test_get_scholarships_list(client):
    """Test retrieving all active scholarships."""
    response = client.get('/api/scholarships')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]['name'] == 'Test National Scholarship'

def test_get_featured_scholarships(client):
    """Test retrieving featured scholarships."""
    response = client.get('/api/scholarships/featured')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 6

def test_get_single_scholarship(client):
    """Test fetching scholarship by ID."""
    response = client.get('/api/scholarships/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['provider'] == 'Test Ministry'

def test_scholarship_not_found(client):
    """Test fetching nonexistent scholarship returns 404."""
    response = client.get('/api/scholarships/99999')
    assert response.status_code == 404

def test_scholarship_filtering(client):
    """Test query parameter filtering by category and amount."""
    # Match Academic
    res = client.get('/api/scholarships?category=Academic')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1

    # Match non-existent category
    res_empty = client.get('/api/scholarships?category=NonExistentCategoryXYZ')
    assert res_empty.status_code == 200
    assert len(res_empty.get_json()) == 0

    # Search keyword
    res_search = client.get('/api/scholarships?search=National')
    assert res_search.status_code == 200
    assert len(res_search.get_json()) >= 1

