"""JSON output formatter."""

import json
import sys
from typing import Any


def format_json(data: Any) -> None:
    """Print data as formatted JSON to stdout."""
    json.dump(data, sys.stdout, indent=2, default=str, ensure_ascii=False)
    sys.stdout.write("\n")
