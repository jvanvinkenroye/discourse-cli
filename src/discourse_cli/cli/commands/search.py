"""Search commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.command("search")
@click.argument("query")
@click.option("--page", type=int, help="Page number.")
@api_command
def search(
    client: DiscourseClient,
    output_format: str,
    query: str,
    page: int | None,
) -> None:
    """Search topics, posts, and users."""
    data = client.search(q=query, page=page)
    # Show topics by default, fall back to full response
    topics = data.get("topics", [])
    posts = data.get("posts", [])
    if topics:
        rows = [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "category_id": t.get("category_id"),
                "posts_count": t.get("posts_count"),
            }
            for t in topics
        ]
        render(rows, output_format, title=f"Search: {query}")
    elif posts:
        render(posts, output_format, title=f"Search: {query}")
    else:
        render(data, output_format, title=f"Search: {query}")
