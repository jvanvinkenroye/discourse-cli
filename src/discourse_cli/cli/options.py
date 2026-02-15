"""Shared CLI decorators and options."""

import functools
import sys
from collections.abc import Callable
from typing import Any

import click

from discourse_cli.api.client import DiscourseClient
from discourse_cli.config.loader import load_config
from discourse_cli.exceptions import ConfigError, DiscourseError
from discourse_cli.formatters.json_fmt import format_json
from discourse_cli.formatters.table_fmt import format_table


def output_option(f: Callable[..., Any]) -> Callable[..., Any]:
    """Add --output / -o option for format selection (auto/json/table)."""
    return click.option(
        "--output",
        "-o",
        "output_format",
        type=click.Choice(["auto", "json", "table"]),
        default="auto",
        help="Output format. 'auto' uses table for TTY, json for pipes.",
    )(f)


def render(data: Any, output_format: str, title: str | None = None) -> None:
    """Render data according to the chosen output format."""
    if output_format == "auto":
        output_format = "table" if sys.stdout.isatty() else "json"

    if output_format == "json":
        format_json(data)
    else:
        format_table(data, title=title)


pass_client = click.make_pass_decorator(DiscourseClient, ensure=True)


class ClientContext:
    """Click context object that lazily creates the API client."""

    def __init__(self) -> None:
        self._client: DiscourseClient | None = None
        self.profile: str | None = None
        self.url: str | None = None
        self.api_key: str | None = None
        self.api_username: str | None = None

    @property
    def client(self) -> DiscourseClient:
        """Build and cache the API client from resolved config."""
        if self._client is None:
            config = load_config(
                url=self.url,
                api_key=self.api_key,
                api_username=self.api_username,
                profile=self.profile,
            )
            self._client = DiscourseClient(config)
        return self._client


pass_context = click.make_pass_decorator(ClientContext, ensure=True)


def api_command(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator combining @pass_context, @output_option, and error handling."""

    @output_option
    @pass_context
    @functools.wraps(f)
    def wrapper(ctx: ClientContext, output_format: str, **kwargs: Any) -> None:
        try:
            f(ctx.client, output_format, **kwargs)
        except ConfigError as e:
            raise click.ClickException(str(e)) from e
        except DiscourseError as e:
            prefix = f"[{e.status_code}] " if e.status_code else ""
            raise click.ClickException(f"{prefix}{e}") from e

    return wrapper
