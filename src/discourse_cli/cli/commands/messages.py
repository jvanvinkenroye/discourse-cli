"""Private message commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("messages")
def messages() -> None:
    """Manage private messages."""


@messages.command("inbox")
@click.argument("username")
@api_command
def inbox(
    client: DiscourseClient, output_format: str, username: str
) -> None:
    """List private messages inbox."""
    data = client.list_user_private_messages(username)
    topic_list = data.get("topic_list", {}).get("topics", data)
    if isinstance(topic_list, list):
        rows = [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "posts_count": t.get("posts_count"),
                "last_posted_at": t.get("last_posted_at"),
            }
            for t in topic_list
        ]
        render(rows, output_format, title=f"Messages: {username}")
    else:
        render(data, output_format, title=f"Messages: {username}")


@messages.command("sent")
@click.argument("username")
@api_command
def sent(
    client: DiscourseClient, output_format: str, username: str
) -> None:
    """List sent private messages."""
    data = client.get_user_sent_private_messages(username)
    topic_list = data.get("topic_list", {}).get("topics", data)
    render(topic_list, output_format, title=f"Sent Messages: {username}")


@messages.command("create")
@click.option("--title", required=True, help="Message subject.")
@click.option("--raw", required=True, help="Message content (markdown).")
@click.option("--target-recipients", required=True,
              help="Comma-separated usernames.")
@api_command
def create_message(
    client: DiscourseClient,
    output_format: str,
    title: str,
    raw: str,
    target_recipients: str,
) -> None:
    """Send a private message."""
    data = client.create_topic_post_pm(
        raw=raw,
        title=title,
        target_recipients=target_recipients,
        archetype="private_message",
    )
    render(data, output_format, title="Message Sent")
