import pytest
import requests

@pytest.fixture
def api_url():
    return "http://127.0.0.1:5000/profile"

def test_successful_response(api_url):
    payload = {"user_id": 1001}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert 'data' in response.json()
    assert len(response.json()['data']) > 0
    user_data = response.json()['data'][0]
    assert 'name' in user_data
    assert 'email' in user_data
    assert 'role' in user_data
    assert 'member_since' in user_data

def test_missing_user_id(api_url):
    payload = {}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 403
    assert response.json()['message'] == 'Please provide a user id.'

def test_user_not_found(api_url):
    payload = {"user_id": 9999}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 404
    assert response.json()['message'] == 'There are no user with user id 9999'

if __name__ == "__main__":
    pytest.main([__file__])
