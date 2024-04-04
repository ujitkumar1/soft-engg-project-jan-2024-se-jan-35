import pytest
import requests

@pytest.fixture
def api_endpoint():
    return "/posts/{id}/locked.json"

@pytest.fixture
def valid_api_key():
    return "your-api-key"  # Replace with your actual API key

@pytest.fixture
def valid_api_username():
    return "your-api-username"  # Replace with your actual API username

@pytest.fixture
def valid_post_id():
    return "123"  # Replace with a valid post ID

def test_lock_post(api_endpoint, valid_api_key, valid_api_username, valid_post_id):
    base_url = "https://localhost:5200" 
    api_url = base_url + api_endpoint.format(id=valid_post_id)
    
    headers = {
        "Api-Key": valid_api_key,
        "Api-Username": valid_api_username,
        "Content-Type": "application/json"
    }
    
    payload = {
        "locked": "true"  # Lock the post
    }
    
    response = requests.put(api_url, headers=headers, json=payload)
    
    assert response.status_code == 200
    assert "locked" in response.json()
    assert response.json()["locked"] == True


