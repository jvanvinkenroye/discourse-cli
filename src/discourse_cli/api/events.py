"""Discourse API: Discourse Calendar - Events endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class EventsMixin:
    """API methods for Discourse Calendar - Events.

    Requires BaseClient.request() via mixin composition.
    """

    def list_events(self, *, include_details: str | None = None, category_id: int | None = None, include_subcategories: str | None = None, post_id: int | None = None, attending_user: str | None = None, before: str | None = None, after: str | None = None, order: str | None = None, limit: int | None = None) -> dict:
        """List calendar events

        GET /discourse-post-event/events.json
        """
        _path_params = None
        _query_params = {"include_details": include_details, "category_id": category_id, "include_subcategories": include_subcategories, "post_id": post_id, "attending_user": attending_user, "before": before, "after": after, "order": order, "limit": limit}
        _json_body = None
        return self.request(
            "GET",
            "/discourse-post-event/events.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def export_events_ics(self, *, category_id: int | None = None, include_subcategories: str | None = None, attending_user: str | None = None, before: str | None = None, after: str | None = None, order: str | None = None, limit: int | None = None) -> dict:
        """Export calendar events in iCalendar format

        GET /discourse-post-event/events.ics
        """
        _path_params = None
        _query_params = {"category_id": category_id, "include_subcategories": include_subcategories, "attending_user": attending_user, "before": before, "after": after, "order": order, "limit": limit}
        _json_body = None
        return self.request(
            "GET",
            "/discourse-post-event/events.ics",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
