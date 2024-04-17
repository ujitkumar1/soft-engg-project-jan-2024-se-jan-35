import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


@pytest.mark.parametrize("category, tag, expected_status_code, expected_message", [
    ("python", "quiz-2", 200, None),
    ("python", "", 400, "Invalid request. Please provide a valid tag."),
    ("", "quiz-2", 400, "Invalid request. Please provide a valid category."),
    ("java", "quiz-2", 404, "No discussions found for the provided tag."),
    ("python", "exam", 404, "No discussions found for the provided tag."),
    ("nonexistent_category", "quiz-2", 404, "No discussions found for the provided category."),
    ("python", "nonexistent_tag", 404, "No discussions found for the provided tag."),
    ("", "", 400, "Invalid request. Please provide a valid category."),
    ("nonexistent_category", "", 400, "Invalid request. Please provide a valid category."),
    ("", "nonexistent_tag", 400, "Invalid request. Please provide a valid tag."),
    ("nonexistent_category", "nonexistent_tag", 404, "No discussions found for the provided category."),
])
def test_search_discussions_by_category(category, tag, expected_status_code, expected_message):
    params = {"category": category, "tag": tag}
    url = f"{BASE_URL}/api/search_discussions_by_category"
    response = requests.get(url, params=params)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.json()
        assert isinstance(response.json(), list)
        for discussion in response.json():
            assert "discussion_id" in discussion
            assert "title" in discussion
            assert "description" in discussion
            assert "tags" in discussion
            assert "link" in discussion
    else:
        assert response.json()["message"] == expected_message
