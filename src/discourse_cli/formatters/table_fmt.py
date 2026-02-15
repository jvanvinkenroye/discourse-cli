"""Rich table output formatter."""

from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def format_table(data: Any, title: str | None = None) -> None:
    """Print data as a rich table to the terminal.

    Handles lists of dicts (tabular) and single dicts (key-value).
    """
    if isinstance(data, list) and data and isinstance(data[0], dict):
        _format_list_table(data, title)
    elif isinstance(data, dict):
        _format_dict_table(data, title)
    elif isinstance(data, list):
        _format_simple_list(data, title)
    else:
        console.print(data)


def _format_list_table(
    rows: list[dict[str, Any]], title: str | None
) -> None:
    """Render a list of dicts as a table with columns from keys."""
    if not rows:
        console.print("[dim]No results.[/dim]")
        return

    # Use keys from first row as columns
    columns = list(rows[0].keys())
    table = Table(title=title, show_lines=False)
    for col in columns:
        table.add_column(col, overflow="fold")

    for row in rows:
        table.add_row(*[_cell(row.get(c)) for c in columns])

    console.print(table)


def _format_dict_table(
    data: dict[str, Any], title: str | None
) -> None:
    """Render a single dict as a key-value table."""
    table = Table(title=title, show_header=False)
    table.add_column("Key", style="bold cyan")
    table.add_column("Value")

    for key, value in data.items():
        table.add_row(str(key), _cell(value))

    console.print(table)


def _format_simple_list(
    items: list[Any], title: str | None
) -> None:
    """Render a simple list as numbered rows."""
    table = Table(title=title, show_header=False)
    table.add_column("#", style="dim")
    table.add_column("Value")

    for i, item in enumerate(items, 1):
        table.add_row(str(i), _cell(item))

    console.print(table)


def _cell(value: Any) -> str:
    """Convert a value to a string for table display."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (list, dict)):
        # Truncate complex nested structures
        s = str(value)
        return s[:80] + "..." if len(s) > 80 else s
    return str(value)
