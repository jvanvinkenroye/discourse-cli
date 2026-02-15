"""Topic management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("topics")
def topics() -> None:
    """Manage topics."""


@topics.command("list")
@click.option("--order", help="Sort order.")
@click.option("--ascending", is_flag=True, help="Sort ascending.")
@click.option("--per-page", type=int, help="Results per page.")
@api_command
def list_topics(
    client: DiscourseClient,
    output_format: str,
    order: str | None,
    ascending: bool,
    per_page: int | None,
) -> None:
    """List latest topics."""
    data = client.list_latest_topics(
        order=order,
        ascending="true" if ascending else None,
        per_page=per_page,
    )
    topic_list = data.get("topic_list", {}).get("topics", data)
    if isinstance(topic_list, list):
        rows = [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "category_id": t.get("category_id"),
                "posts_count": t.get("posts_count"),
                "views": t.get("views"),
                "closed": t.get("closed"),
            }
            for t in topic_list
        ]
        render(rows, output_format, title="Latest Topics")
    else:
        render(data, output_format, title="Latest Topics")


@topics.command("top")
@click.option("--period", type=click.Choice(
    ["all", "yearly", "quarterly", "monthly", "weekly", "daily"]
), help="Time period.")
@click.option("--per-page", type=int, help="Results per page.")
@api_command
def top_topics(
    client: DiscourseClient,
    output_format: str,
    period: str | None,
    per_page: int | None,
) -> None:
    """List top topics."""
    data = client.list_top_topics(period=period, per_page=per_page)
    topic_list = data.get("topic_list", {}).get("topics", data)
    render(topic_list, output_format, title="Top Topics")


@topics.command("get")
@click.argument("topic_id")
@api_command
def get_topic(
    client: DiscourseClient, output_format: str, topic_id: str
) -> None:
    """Get a topic by ID."""
    data = client.get_topic(topic_id)
    render(data, output_format, title=f"Topic #{topic_id}")


@topics.command("get-by-external-id")
@click.argument("external_id")
@api_command
def get_by_external_id(
    client: DiscourseClient, output_format: str, external_id: str
) -> None:
    """Get a topic by external ID."""
    data = client.get_topic_by_external_id(external_id)
    render(data, output_format, title=f"Topic (external: {external_id})")


@topics.command("create")
@click.option("--title", required=True, help="Topic title.")
@click.option("--raw", required=True, help="Post content (markdown).")
@click.option("--category", type=int, help="Category ID.")
@click.option("--external-id", help="External ID.")
@api_command
def create_topic(
    client: DiscourseClient,
    output_format: str,
    title: str,
    raw: str,
    category: int | None,
    external_id: str | None,
) -> None:
    """Create a new topic."""
    data = client.create_topic_post_pm(
        raw=raw,
        title=title,
        category=category,
        external_id=external_id,
    )
    render(data, output_format, title="Created Topic")


@topics.command("update")
@click.argument("topic_id")
@click.option("--title", help="New title.")
@click.option("--category-id", type=int, help="New category ID.")
@api_command
def update_topic(
    client: DiscourseClient,
    output_format: str,
    topic_id: str,
    title: str | None,
    category_id: int | None,
) -> None:
    """Update a topic."""
    data = client.update_topic(
        topic_id, title=title, category_id=category_id
    )
    render(data, output_format, title=f"Updated Topic #{topic_id}")


@topics.command("delete")
@click.argument("topic_id")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def delete_topic(
    client: DiscourseClient,
    output_format: str,
    topic_id: str,
    yes: bool,
) -> None:
    """Delete a topic."""
    if not yes:
        click.confirm(f"Delete topic #{topic_id}?", abort=True)
    data = client.remove_topic(topic_id)
    render(data, output_format, title="Deleted Topic")


@topics.command("status")
@click.argument("topic_id")
@click.option("--status", "status_", required=True,
              type=click.Choice(["closed", "archived", "visible", "pinned"]),
              help="Status to change.")
@click.option("--enabled/--disabled", required=True,
              help="Enable or disable the status.")
@click.option("--until", help="Until date (for pinned).")
@api_command
def update_status(
    client: DiscourseClient,
    output_format: str,
    topic_id: str,
    status_: str,
    enabled: bool,
    until: str | None,
) -> None:
    """Update topic status (close, archive, pin, etc.)."""
    data = client.update_topic_status(
        topic_id,
        status=status_,
        enabled="true" if enabled else "false",
        until=until,
    )
    render(data, output_format, title=f"Topic #{topic_id} Status Updated")


@topics.command("timer")
@click.argument("topic_id")
@click.option("--time", "time_", help="Timer time.")
@click.option("--status-type", help="Timer type (e.g. close, open, etc.).")
@click.option("--category-id", type=int, help="Move to category ID.")
@api_command
def set_timer(
    client: DiscourseClient,
    output_format: str,
    topic_id: str,
    time_: str | None,
    status_type: str | None,
    category_id: int | None,
) -> None:
    """Set a topic timer."""
    data = client.create_topic_timer(
        topic_id,
        time=time_,
        status_type=status_type,
        category_id=category_id,
    )
    render(data, output_format, title=f"Timer Set for Topic #{topic_id}")


@topics.command("invite")
@click.argument("topic_id")
@click.option("--user", help="Username to invite.")
@click.option("--email", help="Email to invite.")
@api_command
def invite_to_topic(
    client: DiscourseClient,
    output_format: str,
    topic_id: str,
    user: str | None,
    email: str | None,
) -> None:
    """Invite a user to a topic."""
    data = client.invite_to_topic(topic_id, user=user, email=email)
    render(data, output_format, title="Invited to Topic")


@topics.command("bookmark")
@click.argument("topic_id")
@api_command
def bookmark_topic(
    client: DiscourseClient, output_format: str, topic_id: str
) -> None:
    """Bookmark a topic."""
    data = client.bookmark_topic(topic_id)
    render(data, output_format, title="Topic Bookmarked")


@topics.command("notification-level")
@click.argument("topic_id")
@click.option("--level", required=True,
              type=click.Choice(["0", "1", "2", "3"]),
              help="0=muted, 1=normal, 2=tracking, 3=watching.")
@api_command
def notification_level(
    client: DiscourseClient,
    output_format: str,
    topic_id: str,
    level: str,
) -> None:
    """Set notification level for a topic."""
    data = client.set_notification_level(topic_id, notification_level=level)
    render(data, output_format, title="Notification Level Updated")
