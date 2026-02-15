"""Discourse API: Posts endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class PostsMixin:
    """API methods for Posts.

    Requires BaseClient.request() via mixin composition.
    """

    def list_posts(self, *, before: int | None = None) -> dict:
        """List latest posts across topics

        GET /posts.json
        """
        _path_params = None
        _query_params = {"before": before}
        _json_body = None
        return self.request(
            "GET",
            "/posts.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

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

    def get_post(self, id: str) -> dict:
        """Retrieve a single post

        GET /posts/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/posts/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_post(self, id: str, *, raw: str | None = None, edit_reason: str | None = None, bypass_bump: bool | None = None) -> dict:
        """Update a single post

        PUT /posts/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {
            "bypass_bump": bypass_bump,
            "post": {
                "raw": raw,
                "edit_reason": edit_reason,
            },
        }
        return self.request(
            "PUT",
            "/posts/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def delete_post(self, id: int, *, force_destroy: bool | None = None) -> dict:
        """delete a single post

        DELETE /posts/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"force_destroy": force_destroy}
        return self.request(
            "DELETE",
            "/posts/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def post_replies(self, id: str) -> dict:
        """List replies to a post

        GET /posts/{id}/replies.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/posts/{id}/replies.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def lock_post(self, id: str, *, locked: str) -> dict:
        """Lock a post from being edited

        PUT /posts/{id}/locked.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"locked": locked}
        return self.request(
            "PUT",
            "/posts/{id}/locked.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def perform_post_action(self, *, id: int, post_action_type_id: int, flag_topic: bool | None = None) -> dict:
        """Like a post and other actions

        POST /post_actions.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"id": id, "post_action_type_id": post_action_type_id, "flag_topic": flag_topic}
        return self.request(
            "POST",
            "/post_actions.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
