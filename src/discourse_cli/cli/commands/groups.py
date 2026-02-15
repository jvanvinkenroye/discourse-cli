"""Group management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("groups")
def groups() -> None:
    """Manage groups."""


@groups.command("list")
@api_command
def list_groups(
    client: DiscourseClient, output_format: str
) -> None:
    """List all groups."""
    data = client.list_groups()
    group_list = data.get("groups", data)
    if isinstance(group_list, list):
        rows = [
            {
                "id": g.get("id"),
                "name": g.get("name"),
                "full_name": g.get("full_name", ""),
                "user_count": g.get("user_count"),
                "visibility_level": g.get("visibility_level"),
            }
            for g in group_list
        ]
        render(rows, output_format, title="Groups")
    else:
        render(data, output_format, title="Groups")


@groups.command("get")
@click.argument("name")
@api_command
def get_group(
    client: DiscourseClient, output_format: str, name: str
) -> None:
    """Get a group by name."""
    data = client.get_group(name)
    group = data.get("group", data)
    render(group, output_format, title=f"Group: {name}")


@groups.command("get-by-id")
@click.argument("group_id")
@api_command
def get_group_by_id(
    client: DiscourseClient, output_format: str, group_id: str
) -> None:
    """Get a group by ID."""
    data = client.get_group_by_id(group_id)
    render(data, output_format, title=f"Group #{group_id}")


@groups.command("create")
@click.option("--name", required=True, help="Group name.")
@click.option("--full-name", help="Full display name.")
@click.option("--bio-raw", help="Group bio (markdown).")
@click.option("--visibility-level", type=int, help="Visibility level.")
@click.option("--primary-group", is_flag=True, help="Set as primary group.")
@api_command
def create_group(
    client: DiscourseClient,
    output_format: str,
    name: str,
    full_name: str | None,
    bio_raw: str | None,
    visibility_level: int | None,
    primary_group: bool,
) -> None:
    """Create a new group."""
    data = client.create_group(
        name=name,
        full_name=full_name,
        bio_raw=bio_raw,
        visibility_level=visibility_level,
        primary_group=primary_group or None,
    )
    render(data, output_format, title="Created Group")


@groups.command("delete")
@click.argument("group_id", type=int)
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def delete_group(
    client: DiscourseClient, output_format: str, group_id: int, yes: bool
) -> None:
    """Delete a group."""
    if not yes:
        click.confirm(f"Delete group #{group_id}?", abort=True)
    data = client.delete_group(group_id)
    render(data, output_format, title="Deleted Group")


@groups.command("update")
@click.argument("group_id", type=int)
@click.option("--name", help="Group name.")
@click.option("--full-name", help="Full display name.")
@click.option("--bio-raw", help="Group bio.")
@click.option("--visibility-level", type=int, help="Visibility level.")
@api_command
def update_group(
    client: DiscourseClient,
    output_format: str,
    group_id: int,
    name: str | None,
    full_name: str | None,
    bio_raw: str | None,
    visibility_level: int | None,
) -> None:
    """Update a group."""
    data = client.update_group(
        group_id,
        name=name,
        full_name=full_name,
        bio_raw=bio_raw,
        visibility_level=visibility_level,
    )
    render(data, output_format, title=f"Updated Group #{group_id}")


@groups.command("members")
@click.argument("name")
@api_command
def list_members(
    client: DiscourseClient, output_format: str, name: str
) -> None:
    """List group members."""
    data = client.list_group_members(name)
    members = data.get("members", data)
    if isinstance(members, list):
        rows = [
            {
                "id": m.get("id"),
                "username": m.get("username"),
                "name": m.get("name", ""),
            }
            for m in members
        ]
        render(rows, output_format, title=f"Members of {name}")
    else:
        render(data, output_format, title=f"Members of {name}")


@groups.command("add-members")
@click.argument("group_id", type=int)
@click.option("--usernames", required=True,
              help="Comma-separated usernames to add.")
@api_command
def add_members(
    client: DiscourseClient,
    output_format: str,
    group_id: int,
    usernames: str,
) -> None:
    """Add members to a group."""
    data = client.add_group_members(group_id, usernames=usernames)
    render(data, output_format, title="Members Added")


@groups.command("remove-members")
@click.argument("group_id", type=int)
@click.option("--usernames", required=True,
              help="Comma-separated usernames to remove.")
@api_command
def remove_members(
    client: DiscourseClient,
    output_format: str,
    group_id: int,
    usernames: str,
) -> None:
    """Remove members from a group."""
    data = client.remove_group_members(group_id, usernames=usernames)
    render(data, output_format, title="Members Removed")
