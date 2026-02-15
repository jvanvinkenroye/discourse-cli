"""Discourse API: Categories endpoints.

Auto-generated from openapi.json - do not edit manually.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class CategoriesMixin:
    """API methods for Categories.

    Requires BaseClient.request() via mixin composition.
    """

    def create_category(self, *, name: str, color: str | None = None, text_color: str | None = None, style_type: str | None = None, emoji: str | None = None, icon: str | None = None, parent_category_id: int | None = None, allow_badges: bool | None = None, slug: str | None = None, topic_featured_links_allowed: bool | None = None, everyone: int | None = None, staff: int | None = None, search_priority: int | None = None, form_template_ids: list[str] | None = None, category_localizations: list[str] | None = None) -> dict:
        """Creates a category

        POST /categories.json
        """
        _path_params = None
        _query_params = None
        _json_body = {
            "name": name,
            "color": color,
            "text_color": text_color,
            "style_type": style_type,
            "emoji": emoji,
            "icon": icon,
            "parent_category_id": parent_category_id,
            "allow_badges": allow_badges,
            "slug": slug,
            "topic_featured_links_allowed": topic_featured_links_allowed,
            "search_priority": search_priority,
            "form_template_ids": form_template_ids,
            "category_localizations": category_localizations,
            "permissions": {
                "everyone": everyone,
                "staff": staff,
            },
        }
        return self.request(
            "POST",
            "/categories.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_categories(self, *, include_subcategories: str | None = None) -> dict:
        """Retrieves a list of categories

        GET /categories.json
        """
        _path_params = None
        _query_params = {"include_subcategories": include_subcategories}
        _json_body = None
        return self.request(
            "GET",
            "/categories.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def update_category(self, id: int, *, name: str, color: str | None = None, text_color: str | None = None, style_type: str | None = None, emoji: str | None = None, icon: str | None = None, parent_category_id: int | None = None, allow_badges: bool | None = None, slug: str | None = None, topic_featured_links_allowed: bool | None = None, everyone: int | None = None, staff: int | None = None, search_priority: int | None = None, form_template_ids: list[str] | None = None, category_localizations: list[str] | None = None) -> dict:
        """Updates a category

        PUT /categories/{id}.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = {
            "name": name,
            "color": color,
            "text_color": text_color,
            "style_type": style_type,
            "emoji": emoji,
            "icon": icon,
            "parent_category_id": parent_category_id,
            "allow_badges": allow_badges,
            "slug": slug,
            "topic_featured_links_allowed": topic_featured_links_allowed,
            "search_priority": search_priority,
            "form_template_ids": form_template_ids,
            "category_localizations": category_localizations,
            "permissions": {
                "everyone": everyone,
                "staff": staff,
            },
        }
        return self.request(
            "PUT",
            "/categories/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def list_category_topics(self, slug: str, id: int) -> dict:
        """List topics

        GET /c/{slug}/{id}.json
        """
        _path_params = {"slug": slug, "id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/c/{slug}/{id}.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

    def get_category(self, id: int) -> dict:
        """Show category

        GET /c/{id}/show.json
        """
        _path_params = {"id": id}
        _query_params = None
        _json_body = None
        return self.request(
            "GET",
            "/c/{id}/show.json",
            path_params=_path_params,
            query_params=_query_params,
            json_body=_json_body,
        )

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
