import pytest
# from application import app

# app needs to be imported
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_activity_status(client):
    response = client.get('/support_staff/activity_status')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for staff_member in response.json():
        assert 'username' in staff_member
        assert 'isActive' in staff_member
        assert 'lastActiveTime' in staff_member
        assert isinstance(staff_member['username'], str)
        assert isinstance(staff_member['isActive'], bool)
        assert isinstance(staff_member['lastActiveTime'], str)  # Assuming ISO 8601 format

def test_get_activity_status_with_invalid_api_key(client):
    headers = {
        'X-API-KEY': 'invalid_api_key'
    }
    response = client.get('/support_staff/activity_status', headers=headers)
    assert response.status_code == 401
    assert 'error' in response.json()
    assert response.json()['error'] == 'Unauthorized'
