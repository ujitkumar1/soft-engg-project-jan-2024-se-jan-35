import pytest
import requests

base_url = 'http://127.0.0.1:5000'


@pytest.mark.parametrize("payload, expected_status, expected_message", [
    ({
         'ticket_id': 3,
         'priority_measure': 6,
         'message': 'Priority measure exceeded 5. Immediate action required!',
         'webhook_url': 'https://chat.googleapis.com/v1/spaces/AAAAaBileJo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FFrC6t9XgrHAZMfZvkWnt5YQ_Tr__01JGly9n5kOFPk'
     }, 200, 'Message posted successfully.'),
    ({
         'priority_measure': 6,
         'message': 'Priority measure exceeded 5. Immediate action required!',
         'webhook_url': 'https://example.com/gchat/webhook'
     }, 400, 'Invalid request body. Please provide valid ticket ID and priority measure.'),
    ({
         'ticket_id': 3,
         'priority_measure': 6,
         'message': 'Priority measure exceeded 5. Immediate action required!',
         'webhook_url': 'https://invalid-url'
     }, 500, 'Internal server error. Please try again later.')
])
def test_send_gchat_msg(payload, expected_status, expected_message):
    response = requests.post(f'{base_url}/api/send_gchat_msg', json=payload)
    assert response.status_code == expected_status
    assert response.json().get('message') == expected_message


@pytest.mark.parametrize("payload, expected_status, expected_message", [
    ({
         'post_id': 123,
         'flag_message': 'This post contains inappropriate content.',
         'user_id': 456,
         'message': 'A post has been flagged. Please check immediately.',
         'webhook_url': 'https://chat.googleapis.com/v1/spaces/AAAAaBileJo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FFrC6t9XgrHAZMfZvkWnt5YQ_Tr__01JGly9n5kOFPk'
     }, 200, 'Message sent to Support Manager about the flagged post.'),
    ({
         'flag_message': 'This post contains inappropriate content.',
         'user_id': 456,
         'message': 'A post has been flagged. Please check immediately.',
         'webhook_url': 'https://chat.googleapis.com/v1/spaces/AAAAaBileJo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FFrC6t9XgrHAZMfZvkWnt5YQ_Tr__01JGly9n5kOFPk'
     }, 400, 'Invalid request body. Please provide valid post ID, flag message, and user ID.'),
    ({
         'post_id': 123,
         'flag_message': 'This post contains inappropriate content.',
         'user_id': 456,
         'webhook_url': 'https://invalid-url'
     }, 500, 'Internal server error. Please try again later.')
])
def test_check_flagged_posts(payload, expected_status, expected_message):
    response = requests.post(f'{base_url}/check_flagged_posts', json=payload)
    assert response.status_code == expected_status
    assert response.json().get('message') == expected_message


@pytest.mark.parametrize("payload, expected_status, expected_message", [
    ({
         'post_id': 123,
         'discussion_links': ['https://example.com/previous_discussion1', 'https://example.com/previous_discussion2']
     }, 200, 'Previous discussion links submitted successfully.'),
    ({
         'discussion_links': ['https://example.com/previous_discussion1', 'https://example.com/previous_discussion2']
     }, 400, 'Invalid request body. Please provide a valid post ID.'),
    ({
         'post_id': 123,
         'discussion_links': ['https://invalid-url']
     }, 500, 'Internal server error. Please try again later.')
])
def test_submit_previous_discussion_links(payload, expected_status, expected_message):
    response = requests.post(f'{base_url}/submit_previous_discussion_links', json=payload)
    assert response.status_code == expected_status
    assert response.json().get('message') == expected_message
