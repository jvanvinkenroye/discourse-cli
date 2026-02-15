"""Configuration management commands: init, show, validate."""

import click
from rich.console import Console

from discourse_cli.api.client import DiscourseClient
from discourse_cli.config.loader import CONFIG_FILE, load_config, save_config
from discourse_cli.config.models import DiscourseConfig
from discourse_cli.exceptions import ConfigError, DiscourseError

console = Console()


@click.group("config")
def config() -> None:
    """Manage Discourse CLI configuration."""


@config.command()
def init() -> None:
    """Create configuration file interactively."""
    console.print(f"[bold]Discourse CLI Configuration[/bold]\n")

    if CONFIG_FILE.exists():
        if not click.confirm(f"Config file {CONFIG_FILE} exists. Overwrite?"):
            raise click.Abort()

    url = click.prompt("Discourse URL", type=str)
    api_key = click.prompt("API Key", type=str, hide_input=True)
    api_username = click.prompt("API Username", default="system", type=str)

    cfg = {
        "url": url.rstrip("/"),
        "api_key": api_key,
        "api_username": api_username,
        "timeout": 30,
        "default_output": "auto",
    }

    # Validate before saving
    try:
        DiscourseConfig(**cfg)
    except Exception as e:
        raise click.ClickException(f"Invalid configuration: {e}") from e

    path = save_config(cfg)
    console.print(f"\n[green]Config saved to {path}[/green]")


@config.command()
def show() -> None:
    """Show current configuration (with masked API key)."""
    try:
        cfg = load_config()
    except ConfigError as e:
        raise click.ClickException(str(e)) from e

    console.print(f"[bold]url:[/bold]            {cfg.url}")
    masked_key = cfg.api_key[:4] + "..." + cfg.api_key[-4:]
    console.print(f"[bold]api_key:[/bold]        {masked_key}")
    console.print(f"[bold]api_username:[/bold]   {cfg.api_username}")
    console.print(f"[bold]timeout:[/bold]        {cfg.timeout}")
    console.print(f"[bold]default_output:[/bold] {cfg.default_output}")
    console.print(f"\n[dim]Config file: {CONFIG_FILE}[/dim]")


@config.command()
def validate() -> None:
    """Validate configuration by testing the connection."""
    try:
        cfg = load_config()
    except ConfigError as e:
        raise click.ClickException(str(e)) from e

    console.print(f"Testing connection to [bold]{cfg.url}[/bold]...")

    try:
        client = DiscourseClient(cfg)
        result = client.request("GET", "/site/basic-info.json")
        title = result.get("title", "Unknown")
        console.print(f"[green]Connected to: {title}[/green]")
        client.close()
    except DiscourseError as e:
        raise click.ClickException(f"Connection failed: {e}") from e
