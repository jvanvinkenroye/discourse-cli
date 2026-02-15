"""Discourse API: Badges endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class BadgesMixin:
    """API methods for Badges.

    Requires BaseClient.request() via mixin composition.
    """

    def admin_list_badges(self) -> dict:
        """List badges

        GET /admin/badges.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/admin/badges.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def create_badge(self, *, name: str, badge_type_id: int) -> dict:
        """Create badge

        POST /admin/badges.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"name": name, "badge_type_id": badge_type_id}
        return self.request(
            "POST",
            "/admin/badges.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_badge(self, id: int, *, name: str, badge_type_id: int) -> dict:
        """Update badge

        PUT /admin/badges/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"name": name, "badge_type_id": badge_type_id}
        return self.request(
            "PUT",
            "/admin/badges/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def delete_badge(self, id: int) -> dict:
        """Delete badge

        DELETE /admin/badges/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "DELETE",
            "/admin/badges/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_user_badges(self, username: str) -> dict:
        """List badges for a user

        GET /user-badges/{username}.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/user-badges/{username}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
