"""Tag management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("tags")
def tags() -> None:
    """Manage tags."""


@tags.command("list")
@api_command
def list_tags(client: DiscourseClient, output_format: str) -> None:
    """List all tags."""
    data = client.list_tags()
    tag_list = data.get("tags", data)
    if isinstance(tag_list, list):
        rows = [
            {
                "id": t.get("id"),
                "name": t.get("name", t.get("text", "")),
                "count": t.get("count", t.get("topic_count", "")),
            }
            for t in tag_list
        ]
        render(rows, output_format, title="Tags")
    else:
        render(data, output_format, title="Tags")


@tags.command("get")
@click.argument("name")
@api_command
def get_tag(
    client: DiscourseClient, output_format: str, name: str
) -> None:
    """Get a tag by name."""
    data = client.get_tag(name)
    render(data, output_format, title=f"Tag: {name}")


@tags.command("groups")
@api_command
def list_tag_groups(
    client: DiscourseClient, output_format: str
) -> None:
    """List tag groups."""
    data = client.list_tag_groups()
    render(data, output_format, title="Tag Groups")


@tags.command("group-get")
@click.argument("group_id")
@api_command
def get_tag_group(
    client: DiscourseClient, output_format: str, group_id: str
) -> None:
    """Get a tag group by ID."""
    data = client.get_tag_group(group_id)
    render(data, output_format, title=f"Tag Group #{group_id}")


@tags.command("group-create")
@click.option("--name", required=True, help="Tag group name.")
@api_command
def create_tag_group(
    client: DiscourseClient, output_format: str, name: str
) -> None:
    """Create a tag group."""
    data = client.create_tag_group(name=name)
    render(data, output_format, title="Created Tag Group")


@tags.command("group-update")
@click.argument("group_id")
@click.option("--name", help="New tag group name.")
@api_command
def update_tag_group(
    client: DiscourseClient,
    output_format: str,
    group_id: str,
    name: str | None,
) -> None:
    """Update a tag group."""
    data = client.update_tag_group(group_id, name=name)
    render(data, output_format, title=f"Updated Tag Group #{group_id}")
