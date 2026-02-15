"""Tests for the HTTP client."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from discourse_cli.api.client import BaseClient, DiscourseClient
from discourse_cli.config.models import DiscourseConfig
from discourse_cli.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


def _mock_response(
    status_code: int = 200,
    json_data: dict | list | None = None,
    text: str = "",
    content: bytes | None = None,
    headers: dict | None = None,
) -> httpx.Response:
    """Create a mock httpx.Response."""
    resp = httpx.Response(
        status_code=status_code,
        json=json_data,
        text=text if not json_data and content is None else None,
        content=content,
        headers=headers or {},
        request=httpx.Request("GET", "https://test.com"),
    )
    return resp


class TestBaseClient:
    """Tests for the base HTTP client."""

    def test_request_success(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(json_data={"title": "Test Forum"})
        with patch.object(client._http, "request", return_value=mock_resp):
            result = client.request("GET", "/site.json")
        assert result == {"title": "Test Forum"}

    def test_request_with_path_params(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(
            json_data={"id": 42, "username": "testuser"}
        )
        with patch.object(client._http, "request", return_value=mock_resp) as m:
            result = client.request(
                "GET",
                "/admin/users/{id}.json",
                path_params={"id": 42},
            )
        # Verify path was interpolated
        call_args = m.call_args
        assert call_args[0][1] == "/admin/users/42.json"
        assert result["id"] == 42

    def test_request_filters_none_query_params(
        self, config: DiscourseConfig
    ) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(json_data=[{"id": 1}])
        with patch.object(client._http, "request", return_value=mock_resp) as m:
            client.request(
                "GET",
                "/admin/users.json",
                query_params={"page": 1, "email": None},
            )
        call_kwargs = m.call_args
        assert call_kwargs.kwargs["params"] == {"page": 1}

    def test_request_filters_none_body_params(
        self, config: DiscourseConfig
    ) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(json_data={"id": 100})
        with patch.object(client._http, "request", return_value=mock_resp) as m:
            client.request(
                "POST",
                "/posts.json",
                json_body={"raw": "hello", "topic_id": 1, "unused": None},
            )
        call_kwargs = m.call_args
        assert call_kwargs.kwargs["json"] == {"raw": "hello", "topic_id": 1}

    def test_auth_headers_configured(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        assert client._http.headers["Api-Key"] == "test-api-key-1234567890"
        assert client._http.headers["Api-Username"] == "system"

    def test_401_raises_auth_error(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(status_code=401, text="Not authorized")
        with patch.object(client._http, "request", return_value=mock_resp):
            with pytest.raises(AuthenticationError):
                client.request("GET", "/test.json")

    def test_404_raises_not_found(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(status_code=404, text="Not found")
        with patch.object(client._http, "request", return_value=mock_resp):
            with pytest.raises(NotFoundError):
                client.request("GET", "/test.json")

    def test_422_raises_validation_error(
        self, config: DiscourseConfig
    ) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(
            status_code=422,
            json_data={"errors": ["Name is required"]},
        )
        with patch.object(client._http, "request", return_value=mock_resp):
            with pytest.raises(ValidationError, match="Name is required"):
                client.request("GET", "/test.json")

    def test_empty_response_returns_empty_dict(
        self, config: DiscourseConfig
    ) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(status_code=200, content=b"")
        with patch.object(client._http, "request", return_value=mock_resp):
            result = client.request("GET", "/test.json")
        assert result == {}

    def test_context_manager(self, config: DiscourseConfig) -> None:
        with DiscourseClient(config) as client:
            assert client is not None


class TestDiscourseClientMethods:
    """Tests that generated mixin methods are available and work."""

    def test_has_admin_methods(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        assert hasattr(client, "admin_get_user")
        assert hasattr(client, "admin_list_users")
        assert hasattr(client, "suspend_user")
        assert hasattr(client, "silence_user")
        assert hasattr(client, "activate_user")

    def test_has_user_methods(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        assert hasattr(client, "get_user")
        assert hasattr(client, "create_user")
        assert hasattr(client, "update_user")
        assert hasattr(client, "delete_user")

    def test_has_topic_methods(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        assert hasattr(client, "get_topic")
        assert hasattr(client, "list_latest_topics")
        assert hasattr(client, "create_topic_post_pm")
        assert hasattr(client, "remove_topic")

    def test_has_group_methods(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        assert hasattr(client, "list_groups")
        assert hasattr(client, "create_group")
        assert hasattr(client, "add_group_members")

    def test_has_search_method(self, config: DiscourseConfig) -> None:
        client = DiscourseClient(config)
        assert hasattr(client, "search")

    def test_admin_list_users_delegates_to_request(
        self, config: DiscourseConfig
    ) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(
            json_data=[{"id": 1, "username": "admin"}]
        )
        with patch.object(client._http, "request", return_value=mock_resp):
            result = client.admin_list_users(page=1)
        assert result == [{"id": 1, "username": "admin"}]

    def test_get_user_delegates_to_request(
        self, config: DiscourseConfig
    ) -> None:
        client = DiscourseClient(config)
        mock_resp = _mock_response(
            json_data={"user": {"id": 1, "username": "testuser"}}
        )
        with patch.object(client._http, "request", return_value=mock_resp):
            result = client.get_user("testuser")
        assert result["user"]["username"] == "testuser"

    def test_method_count(self, config: DiscourseConfig) -> None:
        """Verify we have a significant number of generated methods."""
        client = DiscourseClient(config)
        methods = [
            m for m in dir(client)
            if not m.startswith("_")
            and m not in ("request", "close", "config")
            and callable(getattr(client, m))
        ]
        # Should have 60+ generated methods
        assert len(methods) >= 60, f"Only {len(methods)} methods found"
