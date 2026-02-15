"""Generic API escape-hatch command.

Provides direct access to any Discourse API endpoint:
    discourse api GET /site.json
    discourse api POST /posts.json --data '{"raw": "hello", "topic_id": 1}'
    discourse api --list
"""

import json

import click

from discourse_cli.cli.options import (
    ClientContext,
    output_option,
    pass_context,
    render,
)
from discourse_cli.exceptions import ConfigError, DiscourseError


@click.command("api")
@click.argument("method", required=False,
                type=click.Choice(["GET", "POST", "PUT", "DELETE", "PATCH"],
                                  case_sensitive=False))
@click.argument("path", required=False)
@click.option("--param", "-p", multiple=True,
              help="Query parameter as key=value. Repeatable.")
@click.option("--data", "-d", help="JSON request body (string or @file).")
@click.option("--list", "list_endpoints", is_flag=True,
              help="List all available API endpoints.")
@output_option
@pass_context
def api_cmd(
    ctx: ClientContext,
    output_format: str,
    method: str | None,
    path: str | None,
    param: tuple[str, ...],
    data: str | None,
    list_endpoints: bool,
) -> None:
    """Generic API call - direct access to any endpoint.

    Examples:

        discourse api GET /site.json

        discourse api POST /posts.json -d '{"raw": "hello", "topic_id": 1}'

        discourse api GET /admin/users.json -p page=1 -p show_emails=true

        discourse api --list
    """
    if list_endpoints:
        _list_endpoints()
        return

    if not method or not path:
        raise click.UsageError(
            "METHOD and PATH are required. "
            "Use 'discourse api GET /path.json' or 'discourse api --list'."
        )

    # Parse query params
    query_params: dict[str, str] = {}
    for p in param:
        if "=" not in p:
            raise click.UsageError(f"Invalid param format: {p} (use key=value)")
        key, value = p.split("=", 1)
        query_params[key] = value

    # Parse body
    json_body = None
    if data:
        if data.startswith("@"):
            filepath = data[1:]
            try:
                with open(filepath) as f:
                    json_body = json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                raise click.UsageError(f"Failed to read {filepath}: {e}") from e
        else:
            try:
                json_body = json.loads(data)
            except json.JSONDecodeError as e:
                raise click.UsageError(f"Invalid JSON body: {e}") from e

    try:
        client = ctx.client
        result = client.request(
            method.upper(),
            path,
            query_params=query_params or None,
            json_body=json_body,
        )
        render(result, output_format)
    except ConfigError as e:
        raise click.ClickException(str(e)) from e
    except DiscourseError as e:
        prefix = f"[{e.status_code}] " if e.status_code else ""
        raise click.ClickException(f"{prefix}{e}") from e


def _list_endpoints() -> None:
    """Print all available API endpoints from the openapi.json."""
    from pathlib import Path

    spec_path = Path(__file__).resolve().parents[3] / "openapi.json"

    # Try package-relative first, then project root
    if not spec_path.exists():
        spec_path = Path(__file__).resolve().parents[4] / "openapi.json"

    if not spec_path.exists():
        click.echo("openapi.json not found. Listing generated methods instead.")
        from discourse_cli.api import DiscourseClient
        for name in sorted(dir(DiscourseClient)):
            if not name.startswith("_") and name not in ("request", "close", "config"):
                click.echo(f"  {name}")
        return

    with spec_path.open() as f:
        spec = json.load(f)

    endpoints: list[tuple[str, str, str]] = []
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if method in ("parameters", "summary", "description"):
                continue
            summary = details.get("summary", "")
            tags = ", ".join(details.get("tags", []))
            endpoints.append((method.upper(), path, f"[{tags}] {summary}"))

    endpoints.sort(key=lambda x: (x[1], x[0]))

    for method, path, desc in endpoints:
        click.echo(f"  {method:7s} {path:50s} {desc}")

    click.echo(f"\n  Total: {len(endpoints)} endpoints")
