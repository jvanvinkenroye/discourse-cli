"""Base HTTP client for the Discourse API."""

import time
from typing import Any

import httpx

from discourse_cli.config.models import DiscourseConfig
from discourse_cli.exceptions import DiscourseError, RateLimitError, map_http_error

# Generated mixin imports
from discourse_cli.api.admin import AdminMixin
from discourse_cli.api.backups import BackupsMixin
from discourse_cli.api.badges import BadgesMixin
from discourse_cli.api.categories import CategoriesMixin
from discourse_cli.api.events import EventsMixin
from discourse_cli.api.groups import GroupsMixin
from discourse_cli.api.invites import InvitesMixin
from discourse_cli.api.notifications import NotificationsMixin
from discourse_cli.api.posts import PostsMixin
from discourse_cli.api.private_messages import PrivateMessagesMixin
from discourse_cli.api.search import SearchMixin
from discourse_cli.api.site import SiteMixin
from discourse_cli.api.tags import TagsMixin
from discourse_cli.api.topics import TopicsMixin
from discourse_cli.api.uploads import UploadsMixin
from discourse_cli.api.users import UsersMixin

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


class BaseClient:
    """Low-level HTTP client with auth, error mapping, and rate-limit retry."""

    def __init__(self, config: DiscourseConfig) -> None:
        self.config = config
        self._http = httpx.Client(
            base_url=config.url,
            headers={
                "Api-Key": config.api_key,
                "Api-Username": config.api_username,
                "Accept": "application/json",
            },
            timeout=config.timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Execute an API request with error handling and rate-limit retry.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: URL path template (e.g. '/users/{id}.json').
            path_params: Values to interpolate into the path.
            query_params: Query string parameters (None values filtered).
            json_body: JSON request body (None values filtered).

        Returns:
            Parsed JSON response.

        Raises:
            DiscourseError: On API errors.
        """
        if path_params:
            for key, value in path_params.items():
                path = path.replace(f"{{{key}}}", str(value))

        params = (
            {k: v for k, v in query_params.items() if v is not None}
            if query_params
            else None
        )
        body = (
            {k: v for k, v in json_body.items() if v is not None}
            if json_body
            else None
        )

        for attempt in range(MAX_RETRIES):
            try:
                response = self._http.request(
                    method,
                    path,
                    params=params,
                    json=body,
                )
            except httpx.HTTPError as e:
                raise DiscourseError(f"HTTP request failed: {e}") from e

            if response.status_code == 429:
                retry_after = int(
                    response.headers.get("Retry-After", RETRY_BACKOFF)
                )
                if attempt < MAX_RETRIES - 1:
                    time.sleep(retry_after)
                    continue
                raise RateLimitError(
                    "Rate limit exceeded", retry_after=retry_after
                )

            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict):
                        message = (
                            error_data.get("error_type", "")
                            or ", ".join(error_data.get("errors", []))
                            or response.text
                        )
                    else:
                        message = response.text
                except Exception:
                    message = response.text
                raise map_http_error(response.status_code, message)

            if not response.content:
                return {}

            try:
                return response.json()
            except Exception:
                return {"raw": response.text}

        return {}

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> "BaseClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class DiscourseClient(AdminMixin, BackupsMixin, BadgesMixin, CategoriesMixin, EventsMixin, GroupsMixin, InvitesMixin, NotificationsMixin, PostsMixin, PrivateMessagesMixin, SearchMixin, SiteMixin, TagsMixin, TopicsMixin, UploadsMixin, UsersMixin, BaseClient):
    """Full Discourse API client - composed from generated mixins."""
