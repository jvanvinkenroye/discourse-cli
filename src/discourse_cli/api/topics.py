"""Discourse API: Topics endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class TopicsMixin:
    """API methods for Topics.

    Requires BaseClient.request() via mixin composition.
    """

    def create_topic_post_pm(self, *, raw: str, title: str | None = None, topic_id: int | None = None, category: int | None = None, target_recipients: str | None = None, target_usernames: str | None = None, archetype: str | None = None, created_at: str | None = None, reply_to_post_number: int | None = None, embed_url: str | None = None, external_id: str | None = None, auto_track: bool | None = None) -> dict:
        """Creates a new topic, a new post, or a private message

        POST /posts.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"title": title, "raw": raw, "topic_id": topic_id, "category": category, "target_recipients": target_recipients, "target_usernames": target_usernames, "archetype": archetype, "created_at": created_at, "reply_to_post_number": reply_to_post_number, "embed_url": embed_url, "external_id": external_id, "auto_track": auto_track}
        return self.request(
            "POST",
            "/posts.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_specific_posts_from_topic(self, id: str, *, post_ids: int) -> dict:
        """Get specific posts from a topic

        GET /t/{id}/posts.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"post_ids[]": post_ids}
        return self.request(
            "GET",
            "/t/{id}/posts.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_topic(self, id: str) -> dict:
        """Get a single topic

        GET /t/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/t/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def remove_topic(self, id: str) -> dict:
        """Remove a topic

        DELETE /t/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "DELETE",
            "/t/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_topic(self, id: str, *, title: str | None = None, category_id: int | None = None) -> dict:
        """Update a topic

        PUT /t/-/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {
            "topic": {
                "title": title,
                "category_id": category_id,
            },
        }
        return self.request(
            "PUT",
            "/t/-/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def invite_to_topic(self, id: str, *, user: str | None = None, email: str | None = None) -> dict:
        """Invite to topic

        POST /t/{id}/invite.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"user": user, "email": email}
        return self.request(
            "POST",
            "/t/{id}/invite.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def invite_group_to_topic(self, id: str, *, group: str | None = None, should_notify: bool | None = None) -> dict:
        """Invite group to topic

        POST /t/{id}/invite-group.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"group": group, "should_notify": should_notify}
        return self.request(
            "POST",
            "/t/{id}/invite-group.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def bookmark_topic(self, id: str) -> dict:
        """Bookmark topic

        PUT /t/{id}/bookmark.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "PUT",
            "/t/{id}/bookmark.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_topic_status(self, id: str, *, status: str, enabled: str, until: str | None = None) -> dict:
        """Update the status of a topic

        PUT /t/{id}/status.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"status": status, "enabled": enabled, "until": until}
        return self.request(
            "PUT",
            "/t/{id}/status.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_latest_topics(self, *, order: str | None = None, ascending: str | None = None, per_page: int | None = None) -> dict:
        """Get the latest topics

        GET /latest.json
        """
        _path_params = None
        _query_params = {"order": order, "ascending": ascending, "per_page": per_page}
        _json_body = None
        return self.request(
            "GET",
            "/latest.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_top_topics(self, *, period: str | None = None, per_page: int | None = None) -> dict:
        """Get the top topics filtered by period

        GET /top.json
        """
        _path_params = None
        _query_params = {"period": period, "per_page": per_page}
        _json_body = None
        return self.request(
            "GET",
            "/top.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def set_notification_level(self, id: str, *, notification_level: str) -> dict:
        """Set notification level

        POST /t/{id}/notifications.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"notification_level": notification_level}
        return self.request(
            "POST",
            "/t/{id}/notifications.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_topic_timestamp(self, id: str, *, timestamp: str) -> dict:
        """Update topic timestamp

        PUT /t/{id}/change-timestamp.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"timestamp": timestamp}
        return self.request(
            "PUT",
            "/t/{id}/change-timestamp.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def create_topic_timer(self, id: str, *, time: str | None = None, status_type: str | None = None, based_on_last_post: bool | None = None, category_id: int | None = None) -> dict:
        """Create topic timer

        POST /t/{id}/timer.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"time": time, "status_type": status_type, "based_on_last_post": based_on_last_post, "category_id": category_id}
        return self.request(
            "POST",
            "/t/{id}/timer.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_topic_by_external_id(self, external_id: str) -> dict:
        """Get topic by external_id

        GET /t/external_id/{external_id}.json
        """
        _path_params = {"external_id": external_id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/t/external_id/{external_id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
