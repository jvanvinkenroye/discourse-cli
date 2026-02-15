"""Site information commands."""

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.cli.options import api_command, render


@click.group("site")
def site() -> None:
    """Site information and settings."""


@site.command("info")
@api_command
def site_info(client: DiscourseClient, output_format: str) -> None:
    """Get basic site information."""
    data = client.get_site_basic_info()
    render(data, output_format, title="Site Info")


@site.command("full")
@api_command
def site_full(client: DiscourseClient, output_format: str) -> None:
    """Get full site configuration."""
    data = client.get_site()
    render(data, output_format, title="Site Configuration")
