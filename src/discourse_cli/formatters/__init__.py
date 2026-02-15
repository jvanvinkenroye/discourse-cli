"""Output formatters for Discourse CLI."""

from discourse_cli.formatters.json_fmt import format_json
from discourse_cli.formatters.table_fmt import format_table

__all__ = ["format_json", "format_table"]
