"""Backup management commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("backups")
def backups() -> None:
    """Manage backups."""


@backups.command("list")
@api_command
def list_backups(client: DiscourseClient, output_format: str) -> None:
    """List all backups."""
    data = client.get_backups()
    if isinstance(data, list):
        rows = [
            {
                "filename": b.get("filename"),
                "size": b.get("size"),
                "link": b.get("link"),
            }
            for b in data
        ]
        render(rows, output_format, title="Backups")
    else:
        render(data, output_format, title="Backups")


@backups.command("create")
@click.option("--with-uploads/--no-uploads", default=True,
              help="Include uploads in backup.")
@api_command
def create_backup(
    client: DiscourseClient, output_format: str, with_uploads: bool
) -> None:
    """Create a new backup."""
    data = client.create_backup(with_uploads=with_uploads)
    render(data, output_format, title="Backup Created")


@backups.command("send-email")
@click.argument("filename")
@api_command
def send_email(
    client: DiscourseClient, output_format: str, filename: str
) -> None:
    """Send download link email for a backup."""
    data = client.send_download_backup_email(filename)
    render(data, output_format, title="Download Email Sent")
