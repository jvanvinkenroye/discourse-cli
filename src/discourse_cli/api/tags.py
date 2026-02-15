"""Discourse API: Tags endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class TagsMixin:
    """API methods for Tags.

    Requires BaseClient.request() via mixin composition.
    """

    def list_tag_groups(self) -> dict:
        """Get a list of tag groups

        GET /tag_groups.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/tag_groups.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def create_tag_group(self, *, name: str) -> dict:
        """Creates a tag group

        POST /tag_groups.json
        """
        _path_params = None
        _query_params = None
        _json_body = {"name": name}
        return self.request(
            "POST",
            "/tag_groups.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_tag_group(self, id: str) -> dict:
        """Get a single tag group

        GET /tag_groups/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/tag_groups/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_tag_group(self, id: str, *, name: str | None = None) -> dict:
        """Update tag group

        PUT /tag_groups/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {"name": name}
        return self.request(
            "PUT",
            "/tag_groups/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_tags(self) -> dict:
        """Get a list of tags

        GET /tags.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/tags.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_tag(self, name: str) -> dict:
        """Get a specific tag

        GET /tag/{name}.json
        """
        _path_params = {"name": name}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/tag/{name}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
