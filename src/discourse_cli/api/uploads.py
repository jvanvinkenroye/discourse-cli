"""Discourse API: Uploads endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class UploadsMixin:
    """API methods for Uploads.

    Requires BaseClient.request() via mixin composition.
    """

    def create_upload(self, *, type_: str, user_id: int | None = None, synchronous: bool | None = None, file: str | None = None) -> dict:
        """Creates an upload

        POST /uploads.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"type": type_, "user_id": user_id, "synchronous": synchronous, "file": file}
        return self.request(
            "POST",
            "/uploads.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def generate_presigned_put(self, *, type_: str, file_name: str, file_size: int, sha1_checksum: str | None = None) -> dict:
        """Initiates a direct external upload

        POST /uploads/generate-presigned-put.json
        """
        _path_params = None
        _query_params = None
        _json_body = {
            "type": type_,
            "file_name": file_name,
            "file_size": file_size,
            "metadata": {
                "sha1-checksum": sha1_checksum,
            },
        }
        return self.request(
            "POST",
            "/uploads/generate-presigned-put.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def complete_external_upload(self, *, unique_identifier: str, for_private_message: str | None = None, for_site_setting: str | None = None, pasted: str | None = None) -> dict:
        """Completes a direct external upload

        POST /uploads/complete-external-upload.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"unique_identifier": unique_identifier, "for_private_message": for_private_message, "for_site_setting": for_site_setting, "pasted": pasted}
        return self.request(
            "POST",
            "/uploads/complete-external-upload.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def create_multipart_upload(self, *, upload_type: str, file_name: str, file_size: int, sha1_checksum: str | None = None) -> dict:
        """Creates a multipart external upload

        POST /uploads/create-multipart.json
        """
        _path_params = None
        _query_params = None
        _json_body = {
            "upload_type": upload_type,
            "file_name": file_name,
            "file_size": file_size,
            "metadata": {
                "sha1-checksum": sha1_checksum,
            },
        }
        return self.request(
            "POST",
            "/uploads/create-multipart.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def batch_presign_multipart_parts(self, *, part_numbers: list[str], unique_identifier: str) -> dict:
        """Generates batches of presigned URLs for multipart parts

        POST /uploads/batch-presign-multipart-parts.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"part_numbers": part_numbers, "unique_identifier": unique_identifier}
        return self.request(
            "POST",
            "/uploads/batch-presign-multipart-parts.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def abort_multipart(self, *, external_upload_identifier: str) -> dict:
        """Abort multipart upload

        POST /uploads/abort-multipart.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"external_upload_identifier": external_upload_identifier}
        return self.request(
            "POST",
            "/uploads/abort-multipart.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def complete_multipart(self, *, unique_identifier: str, parts: list[str]) -> dict:
        """Complete multipart upload

        POST /uploads/complete-multipart.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"unique_identifier": unique_identifier, "parts": parts}
        return self.request(
            "POST",
            "/uploads/complete-multipart.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
