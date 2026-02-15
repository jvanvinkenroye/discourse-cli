"""Discourse API: Invites endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class InvitesMixin:
    """API methods for Invites.

    Requires BaseClient.request() via mixin composition.
    """

    def create_invite(self, *, email: str | None = None, skip_email: bool | None = None, custom_message: str | None = None, max_redemptions_allowed: int | None = None, topic_id: int | None = None, group_ids: str | None = None, group_names: str | None = None, expires_at: str | None = None) -> dict:
        """Create an invite

        POST /invites.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"email": email, "skip_email": skip_email, "custom_message": custom_message, "max_redemptions_allowed": max_redemptions_allowed, "topic_id": topic_id, "group_ids": group_ids, "group_names": group_names, "expires_at": expires_at}
        return self.request(
            "POST",
            "/invites.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def create_multiple_invites(self, *, email: str | None = None, skip_email: bool | None = None, custom_message: str | None = None, max_redemptions_allowed: int | None = None, topic_id: int | None = None, group_ids: str | None = None, group_names: str | None = None, expires_at: str | None = None) -> dict:
        """Create multiple invites

        POST /invites/create-multiple.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"email": email, "skip_email": skip_email, "custom_message": custom_message, "max_redemptions_allowed": max_redemptions_allowed, "topic_id": topic_id, "group_ids": group_ids, "group_names": group_names, "expires_at": expires_at}
        return self.request(
            "POST",
            "/invites/create-multiple.json",
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
