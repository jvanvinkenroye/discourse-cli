"""Discourse API: Admin endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class AdminMixin:
    """API methods for Admin.

    Requires BaseClient.request() via mixin composition.
    """

    def admin_get_user(self, id: int) -> dict:
        """Get a user by id

        GET /admin/users/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/admin/users/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def delete_user(self, id: int, *, delete_posts: bool | None = None, block_email: bool | None = None, block_urls: bool | None = None, block_ip: bool | None = None) -> dict:
        """Delete a user

        DELETE /admin/users/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"delete_posts": delete_posts, "block_email": block_email, "block_urls": block_urls, "block_ip": block_ip}
        return self.request(
            "DELETE",
            "/admin/users/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def activate_user(self, id: int) -> dict:
        """Activate a user

        PUT /admin/users/{id}/activate.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "PUT",
            "/admin/users/{id}/activate.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def deactivate_user(self, id: int) -> dict:
        """Deactivate a user

        PUT /admin/users/{id}/deactivate.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "PUT",
            "/admin/users/{id}/deactivate.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def suspend_user(self, id: int, *, suspend_until: str, reason: str, message: str | None = None, post_action: str | None = None) -> dict:
        """Suspend a user

        PUT /admin/users/{id}/suspend.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"suspend_until": suspend_until, "reason": reason, "message": message, "post_action": post_action}
        return self.request(
            "PUT",
            "/admin/users/{id}/suspend.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def silence_user(self, id: int, *, silenced_till: str, reason: str, message: str | None = None, post_action: str | None = None) -> dict:
        """Silence a user

        PUT /admin/users/{id}/silence.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"silenced_till": silenced_till, "reason": reason, "message": message, "post_action": post_action}
        return self.request(
            "PUT",
            "/admin/users/{id}/silence.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def anonymize_user(self, id: int) -> dict:
        """Anonymize a user

        PUT /admin/users/{id}/anonymize.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "PUT",
            "/admin/users/{id}/anonymize.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def log_out_user(self, id: int) -> dict:
        """Log a user out

        POST /admin/users/{id}/log_out.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "POST",
            "/admin/users/{id}/log_out.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def refresh_gravatar(self, username: str) -> dict:
        """Refresh gravatar

        POST /user_avatar/{username}/refresh_gravatar.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = None
        return self.request(
            "POST",
            "/user_avatar/{username}/refresh_gravatar.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def admin_list_users(self, *, order: str | None = None, asc: str | None = None, page: int | None = None, show_emails: bool | None = None, stats: bool | None = None, email: str | None = None, ip: str | None = None) -> dict:
        """List users

        GET /admin/users.json
        """
        _path_params = None
        _query_params = {"order": order, "asc": asc, "page": page, "show_emails": show_emails, "stats": stats, "email": email, "ip": ip}
        _json_body = None
        return self.request(
            "GET",
            "/admin/users.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def admin_list_users_flag(self, flag: str, *, order: str | None = None, asc: str | None = None, page: int | None = None, show_emails: bool | None = None, stats: bool | None = None, email: str | None = None, ip: str | None = None) -> dict:
        """List users by flag

        GET /admin/users/list/{flag}.json
        """
        _path_params = {"flag": flag}
        _query_params = {"order": order, "asc": asc, "page": page, "show_emails": show_emails, "stats": stats, "email": email, "ip": ip}
        _json_body = None
        return self.request(
            "GET",
            "/admin/users/list/{flag}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
