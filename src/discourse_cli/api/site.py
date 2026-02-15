"""Discourse API: Site endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class SiteMixin:
    """API methods for Site.

    Requires BaseClient.request() via mixin composition.
    """

    def get_site(self) -> dict:
        """Get site info

        GET /site.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/site.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_site_basic_info(self) -> dict:
        """Get site basic info

        GET /site/basic-info.json
        """
        _path_params = None
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/site/basic-info.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
