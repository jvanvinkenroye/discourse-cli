"""Discourse API: Users endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class UsersMixin:
    """API methods for Users.

    Requires BaseClient.request() via mixin composition.
    """

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

    def create_user(self, *, name: str, email: str, password: str, username: str, active: bool | None = None, approved: bool | None = None, p_1: bool | None = None, external_ids: dict | None = None) -> dict:
        """Creates a user

        POST /users.json
        """
        _path_params = None
        _query_params = None
        _json_body = {
            "name": name,
            "email": email,
            "password": password,
            "username": username,
            "active": active,
            "approved": approved,
            "external_ids": external_ids,
            "user_fields": {
                "1": p_1,
            },
        }
        return self.request(
            "POST",
            "/users.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_user(self, username: str) -> dict:
        """Get a single user by username

        GET /u/{username}.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/u/{username}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_user(self, username: str, *, name: str | None = None, external_ids: dict | None = None) -> dict:
        """Update a user

        PUT /u/{username}.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = {"name": name, "external_ids": external_ids}
        return self.request(
            "PUT",
            "/u/{username}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_user_external_id(self, external_id: str) -> dict:
        """Get a user by external_id

        GET /u/by-external/{external_id}.json
        """
        _path_params = {"external_id": external_id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/u/by-external/{external_id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_user_identiy_provider_external_id(self, provider: str, external_id: str) -> dict:
        """Get a user by identity provider external ID

        GET /u/by-external/{provider}/{external_id}.json
        """
        _path_params = {"provider": provider, "external_id": external_id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/u/by-external/{provider}/{external_id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_avatar(self, username: str, *, upload_id: int, type_: str) -> dict:
        """Update avatar

        PUT /u/{username}/preferences/avatar/pick.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = {"upload_id": upload_id, "type": type_}
        return self.request(
            "PUT",
            "/u/{username}/preferences/avatar/pick.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_email(self, username: str, *, email: str) -> dict:
        """Update email

        PUT /u/{username}/preferences/email.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = {"email": email}
        return self.request(
            "PUT",
            "/u/{username}/preferences/email.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_username(self, username: str, *, new_username: str) -> dict:
        """Update username

        PUT /u/{username}/preferences/username.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = {"new_username": new_username}
        return self.request(
            "PUT",
            "/u/{username}/preferences/username.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_users_public(self, *, period: str, order: str, asc: str | None = None, page: int | None = None) -> dict:
        """Get a public list of users

        GET /directory_items.json
        """
        _path_params = None
        _query_params = {"period": period, "order": order, "asc": asc, "page": page}
        _json_body = None
        return self.request(
            "GET",
            "/directory_items.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

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

    def list_user_actions(self, *, offset: int, username: str, filter: str) -> dict:
        """Get a list of user actions

        GET /user_actions.json
        """
        _path_params = None
        _query_params = {"offset": offset, "username": username, "filter": filter}
        _json_body = None
        return self.request(
            "GET",
            "/user_actions.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def send_password_reset_email(self, *, login: str) -> dict:
        """Send password reset email

        POST /session/forgot_password.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"login": login}
        return self.request(
            "POST",
            "/session/forgot_password.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def change_password(self, token: str, *, username: str, password: str) -> dict:
        """Change password

        PUT /users/password-reset/{token}.json
        """
        _path_params = {"token": token}
        _query_params = None
        _json_body = {"username": username, "password": password}
        return self.request(
            "PUT",
            "/users/password-reset/{token}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_user_emails(self, username: str) -> dict:
        """Get email addresses belonging to a user

        GET /u/{username}/emails.json
        """
        _path_params = {"username": username}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/u/{username}/emails.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
