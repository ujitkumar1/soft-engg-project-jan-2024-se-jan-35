import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


@pytest.mark.parametrize("tag, expected_status_code, expected_error_message", [
    ("python", 200, None),
    ("java", 404, "No discussions found for the provided tag."),
    ("", 400, "Invalid request. Please provide a valid tag."),
    ("invalid_tag", 400, "Invalid request. Please provide a valid tag."),
])
def test_search_discussions_by_tag(tag, expected_status_code, expected_error_message):
    url = f"{BASE_URL}/api/search_discussions_by_tag?tag={tag}"
    response = requests.get(url)
    
    assert response.status_code == expected_status_code
    
    if response.status_code == 200:
        response_json = response.json()
        assert isinstance(response_json, list)
        for discussion in response_json:
            assert "discussion_id" in discussion
            assert isinstance(discussion["discussion_id"], int)
            assert "title" in discussion
            assert isinstance(discussion["title"], str)
            assert "description" in discussion
            assert isinstance(discussion["description"], str)
            assert "tags" in discussion
            assert isinstance(discussion["tags"], list)
            assert all(isinstance(tag, str) for tag in discussion["tags"])
            assert "link" in discussion
            assert isinstance(discussion["link"], str)
            assert discussion["link"].startswith("http")
    elif response.status_code == 400 or response.status_code == 404:
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert "message" in response_json
        assert response_json["message"] == expected_error_message
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")


if __name__ == "__main__":
    pytest.main()
