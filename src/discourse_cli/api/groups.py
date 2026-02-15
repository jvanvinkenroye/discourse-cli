"""Discourse API: Groups endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class GroupsMixin:
    """API methods for Groups.

    Requires BaseClient.request() via mixin composition.
    """

    def create_group(self, *, name: str | None = None, full_name: str | None = None, bio_raw: str | None = None, usernames: str | None = None, owner_usernames: str | None = None, automatic_membership_email_domains: str | None = None, visibility_level: int | None = None, primary_group: bool | None = None, flair_icon: str | None = None, flair_upload_id: int | None = None, flair_bg_color: str | None = None, public_admission: bool | None = None, public_exit: bool | None = None, default_notification_level: int | None = None, muted_category_ids: list[int] | None = None, regular_category_ids: list[int] | None = None, watching_category_ids: list[int] | None = None, tracking_category_ids: list[int] | None = None, watching_first_post_category_ids: list[int] | None = None) -> dict:
        """Create a group

        POST /admin/groups.json
        """
        _path_params = None
        _query_params = None
        _json_body = {
            "group": {
                "name": name,
                "full_name": full_name,
                "bio_raw": bio_raw,
                "usernames": usernames,
                "owner_usernames": owner_usernames,
                "automatic_membership_email_domains": automatic_membership_email_domains,
                "visibility_level": visibility_level,
                "primary_group": primary_group,
                "flair_icon": flair_icon,
                "flair_upload_id": flair_upload_id,
                "flair_bg_color": flair_bg_color,
                "public_admission": public_admission,
                "public_exit": public_exit,
                "default_notification_level": default_notification_level,
                "muted_category_ids": muted_category_ids,
                "regular_category_ids": regular_category_ids,
                "watching_category_ids": watching_category_ids,
                "tracking_category_ids": tracking_category_ids,
                "watching_first_post_category_ids": watching_first_post_category_ids,
            },
        }
        return self.request(
            "POST",
            "/admin/groups.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def delete_group(self, id: int) -> dict:
        """Delete a group

        DELETE /admin/groups/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "DELETE",
            "/admin/groups/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_group(self, name: str) -> dict:
        """Get a group

        GET /groups/{name}.json
        """
        _path_params = {"name": name}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/groups/{name}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_group(self, id: int, *, name: str | None = None, full_name: str | None = None, bio_raw: str | None = None, usernames: str | None = None, owner_usernames: str | None = None, automatic_membership_email_domains: str | None = None, visibility_level: int | None = None, primary_group: bool | None = None, flair_icon: str | None = None, flair_upload_id: int | None = None, flair_bg_color: str | None = None, public_admission: bool | None = None, public_exit: bool | None = None, default_notification_level: int | None = None, muted_category_ids: list[int] | None = None, regular_category_ids: list[int] | None = None, watching_category_ids: list[int] | None = None, tracking_category_ids: list[int] | None = None, watching_first_post_category_ids: list[int] | None = None) -> dict:
        """Update a group

        PUT /groups/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {
            "group": {
                "name": name,
                "full_name": full_name,
                "bio_raw": bio_raw,
                "usernames": usernames,
                "owner_usernames": owner_usernames,
                "automatic_membership_email_domains": automatic_membership_email_domains,
                "visibility_level": visibility_level,
                "primary_group": primary_group,
                "flair_icon": flair_icon,
                "flair_upload_id": flair_upload_id,
                "flair_bg_color": flair_bg_color,
                "public_admission": public_admission,
                "public_exit": public_exit,
                "default_notification_level": default_notification_level,
                "muted_category_ids": muted_category_ids,
                "regular_category_ids": regular_category_ids,
                "watching_category_ids": watching_category_ids,
                "tracking_category_ids": tracking_category_ids,
                "watching_first_post_category_ids": watching_first_post_category_ids,
            },
        }
        return self.request(
            "PUT",
            "/groups/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_group_by_id(self, id: str) -> dict:
        """Get a group by id

        GET /groups/by-id/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/groups/by-id/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_group_members(self, name: str) -> dict:
        """List group members

        GET /groups/{name}/members.json
        """
        _path_params = {"name": name}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/groups/{name}/members.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def add_group_members(self, id: int, *, usernames: str | None = None) -> dict:
        """Add group members

        PUT /groups/{id}/members.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"usernames": usernames}
        return self.request(
            "PUT",
            "/groups/{id}/members.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def remove_group_members(self, id: int, *, usernames: str | None = None) -> dict:
        """Remove group members

        DELETE /groups/{id}/members.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"usernames": usernames}
        return self.request(
            "DELETE",
            "/groups/{id}/members.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_groups(self) -> dict:
        """List groups

        GET /groups.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/groups.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
