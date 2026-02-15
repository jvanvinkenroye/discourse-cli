"""Category management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("categories")
def categories() -> None:
    """Manage categories."""


@categories.command("list")
@click.option("--include-subcategories", is_flag=True,
              help="Include subcategories.")
@api_command
def list_categories(
    client: DiscourseClient,
    output_format: str,
    include_subcategories: bool,
) -> None:
    """List all categories."""
    data = client.list_categories(
        include_subcategories="true" if include_subcategories else None,
    )
    cats = data.get("category_list", {}).get("categories", data)
    if isinstance(cats, list):
        rows = [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "slug": c.get("slug"),
                "topic_count": c.get("topic_count"),
                "post_count": c.get("post_count"),
                "description": (c.get("description_text", "")[:60] + "..."
                                if len(c.get("description_text", "")) > 60
                                else c.get("description_text", "")),
            }
            for c in cats
        ]
        render(rows, output_format, title="Categories")
    else:
        render(data, output_format, title="Categories")


@categories.command("get")
@click.argument("category_id", type=int)
@api_command
def get_category(
    client: DiscourseClient, output_format: str, category_id: int
) -> None:
    """Get a category by ID."""
    data = client.get_category(category_id)
    render(data, output_format, title=f"Category #{category_id}")


@categories.command("create")
@click.option("--name", required=True, help="Category name.")
@click.option("--color", help="Category color (hex).")
@click.option("--text-color", help="Text color (hex).")
@click.option("--slug", help="Category slug.")
@click.option("--parent-category-id", type=int, help="Parent category ID.")
@api_command
def create_category(
    client: DiscourseClient,
    output_format: str,
    name: str,
    color: str | None,
    text_color: str | None,
    slug: str | None,
    parent_category_id: int | None,
) -> None:
    """Create a new category."""
    data = client.create_category(
        name=name,
        color=color,
        text_color=text_color,
        slug=slug,
        parent_category_id=parent_category_id,
    )
    render(data, output_format, title="Created Category")


@categories.command("update")
@click.argument("category_id", type=int)
@click.option("--name", required=True, help="Category name.")
@click.option("--color", help="Category color (hex).")
@click.option("--text-color", help="Text color (hex).")
@click.option("--slug", help="Category slug.")
@click.option("--parent-category-id", type=int, help="Parent category ID.")
@api_command
def update_category(
    client: DiscourseClient,
    output_format: str,
    category_id: int,
    name: str,
    color: str | None,
    text_color: str | None,
    slug: str | None,
    parent_category_id: int | None,
) -> None:
    """Update a category."""
    data = client.update_category(
        category_id,
        name=name,
        color=color,
        text_color=text_color,
        slug=slug,
        parent_category_id=parent_category_id,
    )
    render(data, output_format, title=f"Updated Category #{category_id}")


@categories.command("topics")
@click.argument("slug")
@click.argument("category_id", type=int)
@api_command
def category_topics(
    client: DiscourseClient,
    output_format: str,
    slug: str,
    category_id: int,
) -> None:
    """List topics in a category."""
    data = client.list_category_topics(slug, category_id)
    topic_list = data.get("topic_list", {}).get("topics", data)
    render(topic_list, output_format, title=f"Topics in {slug}")
