import pytest
import requests
from requests_mock import Mocker
# from application import app

#app needs to be imported
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_send_message(client):
    message_data = {
        "threadId": "thread123",
        "text": "Test message",
        "urgent": True,
        "ticketId": "ticket123"
    }
    response = client.post('/messages', json=message_data)
    assert response.status_code == 201

def test_send_message_invalid_input(client):
    invalid_message_data = {
        "threadId": "thread123",
        # Missing required 'text' field
        "urgent": True,
        "ticketId": "ticket123"
    }
    response = client.post('/messages', json=invalid_message_data)
    assert response.status_code == 400

def test_get_message(client):
    message_id = "message123"
    with Mocker() as m:
        message_data = {
            "threadId": "thread123",
            "text": "Test message",
            "urgent": True,
            "ticketId": "ticket123"
        }
        m.get(f'/messages/{message_id}', json=message_data)
        response = client.get(f'/messages/{message_id}')
        assert response.status_code == 200
        assert response.json() == message_data

def test_get_message_not_found(client):
    message_id = "non_existent_message_id"
    with Mocker() as m:
        m.get(f'/messages/{message_id}', status_code=404)
        response = client.get(f'/messages/{message_id}')
        assert response.status_code == 404
