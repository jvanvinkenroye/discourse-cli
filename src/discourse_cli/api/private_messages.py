"""Discourse API: Private Messages endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class PrivateMessagesMixin:
    """API methods for Private Messages.

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

    def list_user_private_messages(self, username: str) -> dict:
        """Get a list of private messages for a user

        GET /topics/private-messages/{username}.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/topics/private-messages/{username}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_user_sent_private_messages(self, username: str) -> dict:
        """Get a list of private messages sent for a user

        GET /topics/private-messages-sent/{username}.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/topics/private-messages-sent/{username}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
