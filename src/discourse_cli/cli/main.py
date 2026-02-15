"""Root CLI entry point for Discourse CLI."""

import click

from discourse_cli import __version__
from discourse_cli.cli.options import ClientContext


@click.group()
@click.version_option(version=__version__, prog_name="discourse")
@click.option("--url", envvar="DISCOURSE_URL", help="Discourse instance URL.")
@click.option("--api-key", envvar="DISCOURSE_API_KEY", help="API key.")
@click.option(
    "--api-username",
    envvar="DISCOURSE_API_USERNAME",
    default=None,
    help="API username (default: system).",
)
@click.pass_context
def cli(
    ctx: click.Context,
    url: str | None,
    api_key: str | None,
    api_username: str | None,
) -> None:
    """Discourse CLI - Admin tool for Discourse forums."""
    client_ctx = ctx.ensure_object(ClientContext)
    client_ctx.url = url
    client_ctx.api_key = api_key
    client_ctx.api_username = api_username


# Import and register command groups
from discourse_cli.cli.commands.config_cmd import config  # noqa: E402

cli.add_command(config)


def _register_commands() -> None:
    """Register all command groups. Called after generation."""
    # These imports will work once the command modules exist
    command_modules = [
        ("discourse_cli.cli.commands.users", "users"),
        ("discourse_cli.cli.commands.admin", "admin"),
        ("discourse_cli.cli.commands.topics", "topics"),
        ("discourse_cli.cli.commands.posts", "posts"),
        ("discourse_cli.cli.commands.categories", "categories"),
        ("discourse_cli.cli.commands.groups", "groups"),
        ("discourse_cli.cli.commands.tags", "tags"),
        ("discourse_cli.cli.commands.badges", "badges"),
        ("discourse_cli.cli.commands.backups", "backups"),
        ("discourse_cli.cli.commands.invites", "invites"),
        ("discourse_cli.cli.commands.search", "search"),
        ("discourse_cli.cli.commands.site", "site"),
        ("discourse_cli.cli.commands.messages", "messages"),
        ("discourse_cli.cli.commands.notifications", "notifications"),
        ("discourse_cli.cli.commands.uploads", "uploads"),
        ("discourse_cli.cli.commands.api", "api_cmd"),
    ]
    import importlib

    for module_path, attr_name in command_modules:
        try:
            mod = importlib.import_module(module_path)
            cmd = getattr(mod, attr_name, None)
            if cmd:
                cli.add_command(cmd)
        except ImportError:
            pass


_register_commands()
