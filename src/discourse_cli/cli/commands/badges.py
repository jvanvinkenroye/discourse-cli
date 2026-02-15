"""Badge management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("badges")
def badges() -> None:
    """Manage badges."""


@badges.command("list")
@api_command
def list_badges(client: DiscourseClient, output_format: str) -> None:
    """List all badges."""
    data = client.admin_list_badges()
    badge_list = data.get("badges", data)
    if isinstance(badge_list, list):
        rows = [
            {
                "id": b.get("id"),
                "name": b.get("name"),
                "description": b.get("description", ""),
                "badge_type_id": b.get("badge_type_id"),
                "enabled": b.get("enabled"),
            }
            for b in badge_list
        ]
        render(rows, output_format, title="Badges")
    else:
        render(data, output_format, title="Badges")


@badges.command("user")
@click.argument("username")
@api_command
def user_badges(
    client: DiscourseClient, output_format: str, username: str
) -> None:
    """List badges for a user."""
    data = client.list_user_badges(username)
    badge_list = data.get("badges", data)
    render(badge_list, output_format, title=f"Badges: {username}")


@badges.command("create")
@click.option("--name", required=True, help="Badge name.")
@click.option("--badge-type-id", required=True, type=int,
              help="Badge type ID (1=gold, 2=silver, 3=bronze).")
@api_command
def create_badge(
    client: DiscourseClient,
    output_format: str,
    name: str,
    badge_type_id: int,
) -> None:
    """Create a badge."""
    data = client.create_badge(name=name, badge_type_id=badge_type_id)
    render(data, output_format, title="Created Badge")


@badges.command("update")
@click.argument("badge_id", type=int)
@click.option("--name", required=True, help="Badge name.")
@click.option("--badge-type-id", required=True, type=int,
              help="Badge type ID.")
@api_command
def update_badge(
    client: DiscourseClient,
    output_format: str,
    badge_id: int,
    name: str,
    badge_type_id: int,
) -> None:
    """Update a badge."""
    data = client.update_badge(badge_id, name=name, badge_type_id=badge_type_id)
    render(data, output_format, title=f"Updated Badge #{badge_id}")


@badges.command("delete")
@click.argument("badge_id", type=int)
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def delete_badge(
    client: DiscourseClient, output_format: str, badge_id: int, yes: bool
) -> None:
    """Delete a badge."""
    if not yes:
        click.confirm(f"Delete badge #{badge_id}?", abort=True)
    data = client.delete_badge(badge_id)
    render(data, output_format, title="Deleted Badge")
