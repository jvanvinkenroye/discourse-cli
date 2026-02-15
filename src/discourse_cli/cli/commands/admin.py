"""Admin user management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("admin")
def admin() -> None:
    """Admin operations (suspend, silence, activate, etc.)."""


@admin.command()
@click.argument("user_id", type=int)
@api_command
def activate(
    client: DiscourseClient, output_format: str, user_id: int
) -> None:
    """Activate a user."""
    data = client.activate_user(user_id)
    render(data, output_format, title="User Activated")


@admin.command()
@click.argument("user_id", type=int)
@api_command
def deactivate(
    client: DiscourseClient, output_format: str, user_id: int
) -> None:
    """Deactivate a user."""
    data = client.deactivate_user(user_id)
    render(data, output_format, title="User Deactivated")


@admin.command()
@click.argument("user_id", type=int)
@click.option("--until", "suspend_until", required=True,
              help="Suspension end date (YYYY-MM-DD).")
@click.option("--reason", required=True, help="Reason for suspension.")
@click.option("--message", help="Message to the user.")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def suspend(
    client: DiscourseClient,
    output_format: str,
    user_id: int,
    suspend_until: str,
    reason: str,
    message: str | None,
    yes: bool,
) -> None:
    """Suspend a user."""
    if not yes:
        click.confirm(
            f"Suspend user #{user_id} until {suspend_until}?", abort=True
        )
    data = client.suspend_user(
        user_id,
        suspend_until=suspend_until,
        reason=reason,
        message=message,
    )
    render(data, output_format, title="User Suspended")


@admin.command()
@click.argument("user_id", type=int)
@click.option("--until", "silenced_till", required=True,
              help="Silence end date (YYYY-MM-DD).")
@click.option("--reason", required=True, help="Reason for silencing.")
@click.option("--message", help="Message to the user.")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def silence(
    client: DiscourseClient,
    output_format: str,
    user_id: int,
    silenced_till: str,
    reason: str,
    message: str | None,
    yes: bool,
) -> None:
    """Silence a user."""
    if not yes:
        click.confirm(
            f"Silence user #{user_id} until {silenced_till}?", abort=True
        )
    data = client.silence_user(
        user_id,
        silenced_till=silenced_till,
        reason=reason,
        message=message,
    )
    render(data, output_format, title="User Silenced")


@admin.command()
@click.argument("user_id", type=int)
@click.option("--yes", is_flag=True, help="Skip confirmation.")
@api_command
def anonymize(
    client: DiscourseClient, output_format: str, user_id: int, yes: bool
) -> None:
    """Anonymize a user."""
    if not yes:
        click.confirm(
            f"Anonymize user #{user_id}? This cannot be undone!", abort=True
        )
    data = client.anonymize_user(user_id)
    render(data, output_format, title="User Anonymized")


@admin.command("log-out")
@click.argument("user_id", type=int)
@api_command
def log_out(
    client: DiscourseClient, output_format: str, user_id: int
) -> None:
    """Log out a user from all sessions."""
    data = client.log_out_user(user_id)
    render(data, output_format, title="User Logged Out")


@admin.command("refresh-gravatar")
@click.argument("username")
@api_command
def refresh_gravatar(
    client: DiscourseClient, output_format: str, username: str
) -> None:
    """Refresh a user's Gravatar."""
    data = client.refresh_gravatar(username)
    render(data, output_format, title="Gravatar Refreshed")
