"""Discourse API: Search endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class SearchMixin:
    """API methods for Search.

    Requires BaseClient.request() via mixin composition.
    """

    def search(self, *, q: str | None = None, page: int | None = None) -> dict:
        """Search for a term

        GET /search.json
        """
        _path_params = None
        _query_params = {"q": q, "page": page}
        _json_body = None
        return self.request(
            "GET",
            "/search.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )
