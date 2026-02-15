"""Configuration management commands: init, show, validate, list, use."""

import click
from rich.console import Console

from discourse_cli.api.client import DiscourseClient
from discourse_cli.config.loader import (
    CONFIG_FILE,
    get_default_profile,
    list_profiles,
    load_config,
    save_config,
    set_default_profile,
)
from discourse_cli.config.models import DiscourseConfig
from discourse_cli.exceptions import ConfigError, DiscourseError

console = Console()


def _get_profile(ctx: click.Context, explicit_profile: str | None) -> str | None:
    """Resolve the profile name from explicit option or parent --profile flag.

    Returns None when no profile was specified anywhere (flat config mode).
    """
    if explicit_profile is not None:
        return explicit_profile
    # Inherit from parent context (global --profile / -p)
    parent_ctx = ctx.parent
    if parent_ctx and parent_ctx.params.get("profile"):
        return parent_ctx.params["profile"]
    return None


@click.group("config")
def config() -> None:
    """Manage Discourse CLI configuration."""


@config.command()
@click.option(
    "--profile",
    default=None,
    help="Profile name to create (e.g. 'staging'). Creates a named profile.",
)
@click.pass_context
def init(ctx: click.Context, profile: str | None) -> None:
    """Create configuration file interactively."""
    resolved_profile = _get_profile(ctx, profile)
    label = f" [{resolved_profile}]" if resolved_profile else ""
    console.print(f"[bold]Discourse CLI Configuration{label}[/bold]\n")

    if CONFIG_FILE.exists() and not resolved_profile:
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

    path = save_config(cfg, profile=resolved_profile)
    if resolved_profile:
        console.print(
            f"\n[green]Profile '{resolved_profile}' saved to {path}[/green]"
        )
    else:
        console.print(f"\n[green]Config saved to {path}[/green]")


@config.command()
@click.option(
    "--profile",
    default=None,
    help="Profile name to show.",
)
@click.pass_context
def show(ctx: click.Context, profile: str | None) -> None:
    """Show current configuration (with masked API key)."""
    resolved_profile = _get_profile(ctx, profile)
    try:
        cfg = load_config(profile=resolved_profile)
    except ConfigError as e:
        raise click.ClickException(str(e)) from e

    if resolved_profile:
        console.print(f"[bold]Profile:[/bold]        {resolved_profile}")
    else:
        default = get_default_profile()
        if default:
            console.print(f"[bold]Profile:[/bold]        {default} (default)")

    console.print(f"[bold]url:[/bold]            {cfg.url}")
    masked_key = cfg.api_key[:4] + "..." + cfg.api_key[-4:]
    console.print(f"[bold]api_key:[/bold]        {masked_key}")
    console.print(f"[bold]api_username:[/bold]   {cfg.api_username}")
    console.print(f"[bold]timeout:[/bold]        {cfg.timeout}")
    console.print(f"[bold]default_output:[/bold] {cfg.default_output}")
    console.print(f"\n[dim]Config file: {CONFIG_FILE}[/dim]")


@config.command()
@click.option(
    "--profile",
    default=None,
    help="Profile name to validate.",
)
@click.pass_context
def validate(ctx: click.Context, profile: str | None) -> None:
    """Validate configuration by testing the connection."""
    resolved_profile = _get_profile(ctx, profile)
    try:
        cfg = load_config(profile=resolved_profile)
    except ConfigError as e:
        raise click.ClickException(str(e)) from e

    label = f" (profile: {resolved_profile})" if resolved_profile else ""
    console.print(f"Testing connection to [bold]{cfg.url}[/bold]{label}...")

    try:
        client = DiscourseClient(cfg)
        result = client.request("GET", "/site/basic-info.json")
        title = result.get("title", "Unknown")
        console.print(f"[green]Connected to: {title}[/green]")
        client.close()
    except DiscourseError as e:
        raise click.ClickException(f"Connection failed: {e}") from e


@config.command("list")
def list_cmd() -> None:
    """List all configured profiles."""
    profiles = list_profiles()
    default = get_default_profile()

    if not profiles:
        console.print(
            "[dim]No profiles configured. "
            "Config uses flat format or is missing.[/dim]"
        )
        console.print(
            "[dim]Create a profile with: "
            "discourse config init --profile <name>[/dim]"
        )
        return

    console.print("[bold]Configured profiles:[/bold]\n")
    for name in profiles:
        marker = " [green](default)[/green]" if name == default else ""
        console.print(f"  {name}{marker}")


@config.command()
@click.argument("name")
def use(name: str) -> None:
    """Set the default profile.

    NAME is the profile to set as default.
    """
    try:
        set_default_profile(name)
    except ConfigError as e:
        raise click.ClickException(str(e)) from e
    console.print(f"[green]Default profile set to '{name}'.[/green]")
