"""Notification commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("notifications")
def notifications() -> None:
    """Manage notifications."""


@notifications.command("list")
@api_command
def list_notifications(
    client: DiscourseClient, output_format: str
) -> None:
    """List notifications."""
    data = client.get_notifications()
    notifs = data.get("notifications", data)
    if isinstance(notifs, list):
        rows = [
            {
                "id": n.get("id"),
                "type": n.get("notification_type"),
                "read": n.get("read"),
                "created_at": n.get("created_at"),
                "topic_id": n.get("topic_id"),
                "slug": n.get("slug", ""),
            }
            for n in notifs
        ]
        render(rows, output_format, title="Notifications")
    else:
        render(data, output_format, title="Notifications")


@notifications.command("mark-read")
@click.option("--id", "notification_id", type=int,
              help="Specific notification ID. Omit to mark all read.")
@api_command
def mark_read(
    client: DiscourseClient,
    output_format: str,
    notification_id: int | None,
) -> None:
    """Mark notifications as read."""
    data = client.mark_notifications_as_read(id=notification_id)
    render(data, output_format, title="Notifications Marked Read")
