"""Invite management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("invites")
def invites() -> None:
    """Manage invitations."""


@invites.command("create")
@click.option("--email", help="Email to invite.")
@click.option("--skip-email", is_flag=True, help="Don't send invite email.")
@click.option("--custom-message", help="Custom invite message.")
@click.option("--max-redemptions", type=int, help="Max redemptions allowed.")
@click.option("--topic-id", type=int, help="Topic to invite to.")
@click.option("--group-names", help="Comma-separated group names.")
@click.option("--expires-at", help="Expiry date (ISO format).")
@api_command
def create_invite(
    client: DiscourseClient,
    output_format: str,
    email: str | None,
    skip_email: bool,
    custom_message: str | None,
    max_redemptions: int | None,
    topic_id: int | None,
    group_names: str | None,
    expires_at: str | None,
) -> None:
    """Create an invite."""
    data = client.create_invite(
        email=email,
        skip_email=skip_email or None,
        custom_message=custom_message,
        max_redemptions_allowed=max_redemptions,
        topic_id=topic_id,
        group_names=group_names,
        expires_at=expires_at,
    )
    render(data, output_format, title="Invite Created")


@invites.command("bulk")
@click.option("--email", help="Email list (one per line in file).")
@click.option("--group-names", help="Comma-separated group names.")
@click.option("--custom-message", help="Custom message.")
@api_command
def bulk_invite(
    client: DiscourseClient,
    output_format: str,
    email: str | None,
    group_names: str | None,
    custom_message: str | None,
) -> None:
    """Create multiple invites."""
    data = client.create_multiple_invites(
        email=email,
        group_names=group_names,
        custom_message=custom_message,
    )
    render(data, output_format, title="Bulk Invites Created")
