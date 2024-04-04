import pytest
import requests

@pytest.fixture
def valid_payload():
    return {
        "title": "Test Post",
        "raw": "This is a test post.",
        "topic_id": 123,
        "category": 456,
        "created_at": "2024-04-04T12:00:00Z",
        "reply_to_post_number": None
    }

def test_create_post(api_endpoint, valid_payload):
    base_url = "https://localhost:5200//posts.json" 
    api_url = base_url + api_endpoint
    response = requests.post(api_url, json=valid_payload)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()
    assert "username" in response.json()
    assert "avatar_template" in response.json()
    assert "created_at" in response.json()
    assert "raw" in response.json()
    assert "cooked" in response.json()
    assert "post_number" in response.json()
    assert "post_type" in response.json()
    assert "updated_at" in response.json()
    assert "reply_count" in response.json()
    assert "reply_to_post_number" in response.json()
    assert "quote_count" in response.json()
    assert "incoming_link_count" in response.json()
    assert "reads" in response.json()
    assert "readers_count" in response.json()
    assert "score" in response.json()
    assert "yours" in response.json()
    assert "topic_id" in response.json()
    assert "topic_slug" in response.json()
    assert "display_username" in response.json()
    assert "primary_group_name" in response.json()
    assert "flair_name" in response.json()
    assert "flair_url" in response.json()
    assert "flair_bg_color" in response.json()
    assert "flair_color" in response.json()
    assert "version" in response.json()
    assert "can_edit" in response.json()
    assert "can_delete" in response.json()
    assert "can_recover" in response.json()
    assert "can_see_hidden_post" in response.json()
    assert "can_wiki" in response.json()
    assert "user_title" in response.json()
    assert "bookmarked" in response.json()
    assert "actions_summary" in response.json()
    assert "moderator" in response.json()
    assert "admin" in response.json()
    assert "staff" in response.json()
    assert "user_id" in response.json()
    assert "draft_sequence" in response.json()
    assert "hidden" in response.json()
    assert "trust_level" in response.json()
    assert "deleted_at" in response.json()
    assert "user_deleted" in response.json()
    assert "edit_reason" in response.json()
    assert "can_view_edit_history" in response.json()
    assert "wiki" in response.json()
    assert "reviewable_id" in response.json()
    assert "reviewable_score_count" in response.json()
    assert "reviewable_score_pending_count" in response.json()
    assert "mentioned_users" in response.json()

