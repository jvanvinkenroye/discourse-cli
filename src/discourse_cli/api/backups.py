"""Discourse API: Backups endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class BackupsMixin:
    """API methods for Backups.

    Requires BaseClient.request() via mixin composition.
    """

    def get_backups(self) -> dict:
        """List backups

        GET /admin/backups.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/admin/backups.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def create_backup(self, *, with_uploads: bool) -> dict:
        """Create backup

        POST /admin/backups.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"with_uploads": with_uploads}
        return self.request(
            "POST",
            "/admin/backups.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def send_download_backup_email(self, filename: str) -> dict:
        """Send download backup email

        PUT /admin/backups/{filename}
        """
        _path_params = {"filename": filename}
        _query_params = None
        _json_body = None
        return self.request(
            "PUT",
            "/admin/backups/{filename}",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def download_backup(self, filename: str, *, token: str) -> dict:
        """Download backup

        GET /admin/backups/{filename}
        """
        _path_params = {"filename": filename}
        _query_params = {"token": token}
        _json_body = None
        return self.request(
            "GET",
            "/admin/backups/{filename}",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
