"""Post management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("posts")
def posts() -> None:
    """Manage posts."""


@posts.command("list")
@click.option("--before", type=int, help="List posts before this ID.")
@api_command
def list_posts(
    client: DiscourseClient,
    output_format: str,
    before: int | None,
) -> None:
    """List latest posts."""
    data = client.list_posts(before=before)
    post_list = data.get("latest_posts", data)
    if isinstance(post_list, list):
        rows = [
            {
                "id": p.get("id"),
                "topic_id": p.get("topic_id"),
                "username": p.get("username"),
                "created_at": p.get("created_at"),
                "cooked": (p.get("cooked", "")[:80] + "..."
                           if len(p.get("cooked", "")) > 80
                           else p.get("cooked", "")),
            }
            for p in post_list
        ]
        render(rows, output_format, title="Latest Posts")
    else:
        render(data, output_format, title="Latest Posts")


@posts.command("get")
@click.argument("post_id")
@api_command
def get_post(
    client: DiscourseClient, output_format: str, post_id: str
) -> None:
    """Get a post by ID."""
    data = client.get_post(post_id)
    render(data, output_format, title=f"Post #{post_id}")


@posts.command("create")
@click.option("--topic-id", type=int, help="Topic ID to reply to.")
@click.option("--raw", required=True, help="Post content (markdown).")
@click.option("--reply-to", type=int, help="Post number to reply to.")
@api_command
def create_post(
    client: DiscourseClient,
    output_format: str,
    topic_id: int | None,
    raw: str,
    reply_to: int | None,
) -> None:
    """Create a new post (reply to topic)."""
    data = client.create_topic_post_pm(
        raw=raw,
        topic_id=topic_id,
        reply_to_post_number=reply_to,
    )
    render(data, output_format, title="Created Post")


@posts.command("update")
@click.argument("post_id")
@click.option("--raw", help="New post content.")
@click.option("--edit-reason", help="Reason for edit.")
@api_command
def update_post(
    client: DiscourseClient,
    output_format: str,
    post_id: str,
    raw: str | None,
    edit_reason: str | None,
) -> None:
    """Update a post."""
    data = client.update_post(post_id, raw=raw, edit_reason=edit_reason)
    render(data, output_format, title=f"Updated Post #{post_id}")


@posts.command("delete")
@click.argument("post_id", type=int)
@click.option("--force", is_flag=True, help="Force destroy.")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def delete_post(
    client: DiscourseClient,
    output_format: str,
    post_id: int,
    force: bool,
    yes: bool,
) -> None:
    """Delete a post."""
    if not yes:
        click.confirm(f"Delete post #{post_id}?", abort=True)
    data = client.delete_post(post_id, force_destroy=force or None)
    render(data, output_format, title="Deleted Post")


@posts.command("lock")
@click.argument("post_id")
@click.option("--locked/--unlocked", required=True, help="Lock or unlock.")
@api_command
def lock_post(
    client: DiscourseClient,
    output_format: str,
    post_id: str,
    locked: bool,
) -> None:
    """Lock or unlock a post."""
    data = client.lock_post(post_id, locked="true" if locked else "false")
    render(data, output_format, title=f"Post #{post_id} Lock Updated")


@posts.command("replies")
@click.argument("post_id")
@api_command
def post_replies(
    client: DiscourseClient, output_format: str, post_id: str
) -> None:
    """Get replies to a post."""
    data = client.post_replies(post_id)
    render(data, output_format, title=f"Replies to Post #{post_id}")
