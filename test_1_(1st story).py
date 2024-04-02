import json
import pytest
# from application import app

#app needs to be imported
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_post_with_tags(client):
    # Test creating a new post with tags
    post_data = {
        "title": "Test Post",
        "description": "This is a test post",
        "tags": ["user1", "user2"]
    }
    response = client.post('/posts', json=post_data)
    assert response.status_code == 201

def test_create_post_missing_fields(client):
    # Test creating a post with missing fields
    post_data = {
        "description": "This is a test post",
        "tags": ["user1", "user2"]
    }
    response = client.post('/posts', json=post_data)
    assert response.status_code == 400

def test_search_users(client):
    # Test searching for users
    response = client.get('/search_users?search_term=user')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_search_users_no_results(client):
    # Test searching for users with no results
    response = client.get('/search_users?search_term=nonexistentuser')
    assert response.status_code == 404
