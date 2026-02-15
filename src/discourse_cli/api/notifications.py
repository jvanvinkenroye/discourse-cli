"""Discourse API: Notifications endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class NotificationsMixin:
    """API methods for Notifications.

    Requires BaseClient.request() via mixin composition.
    """

    def get_notifications(self) -> dict:
        """Get the notifications that belong to the current user

        GET /notifications.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/notifications.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def mark_notifications_as_read(self, *, id: int | None = None) -> dict:
        """Mark notifications as read

        PUT /notifications/mark-read.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"id": id}
        return self.request(
            "PUT",
            "/notifications/mark-read.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
