import json


def _get_content_from_json_response(response):
    return json.loads(response.content.decode("utf8"))


def assert_no_permission(response):
    content = _get_content_from_json_response(response)
    assert "errors" in content, content
    assert content["errors"][0]["message"] == (
        "You do not have permission to perform this action"
    ), content["errors"]
