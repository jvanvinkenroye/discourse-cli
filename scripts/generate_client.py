#!/usr/bin/env python3
"""Generate typed API mixin modules from openapi.json.

Reads the OpenAPI spec and produces one Python module per API tag
in src/discourse_cli/api/. Each module contains a mixin class with
typed methods that delegate to self.request().

Usage:
    python scripts/generate_client.py
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OPENAPI_PATH = PROJECT_ROOT / "openapi.json"
API_DIR = PROJECT_ROOT / "src" / "discourse_cli" / "api"

# Map OpenAPI tags to Python module names and class names
TAG_MAP: dict[str, tuple[str, str]] = {
    "Admin": ("admin", "AdminMixin"),
    "Backups": ("backups", "BackupsMixin"),
    "Badges": ("badges", "BadgesMixin"),
    "Categories": ("categories", "CategoriesMixin"),
    "Discourse Calendar - Events": ("events", "EventsMixin"),
    "Groups": ("groups", "GroupsMixin"),
    "Invites": ("invites", "InvitesMixin"),
    "Notifications": ("notifications", "NotificationsMixin"),
    "Posts": ("posts", "PostsMixin"),
    "Private Messages": ("private_messages", "PrivateMessagesMixin"),
    "Search": ("search", "SearchMixin"),
    "Site": ("site", "SiteMixin"),
    "Tags": ("tags", "TagsMixin"),
    "Topics": ("topics", "TopicsMixin"),
    "Uploads": ("uploads", "UploadsMixin"),
    "Users": ("users", "UsersMixin"),
}


def camel_to_snake(name: str) -> str:
    """Convert camelCase/PascalCase to snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def parse_type_hint(type_str: str) -> str:
    """Convert extracted type strings to Python type hints."""
    if isinstance(type_str, dict):
        # Nested object - accept as dict
        return "dict"
    if type_str.startswith("array<"):
        inner = type_str[6:-1]
        return f"list[{parse_type_hint(inner)}]"
    if type_str.startswith("string("):
        return "str"
    type_map = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "number": "float",
        "object": "dict",
        "string(binary)": "str",
        "string(date-time)": "str",
    }
    return type_map.get(type_str, "str")


def build_method(endpoint: dict, indent: str = "    ") -> str:
    """Generate a method definition for a single API endpoint.

    All lines are prefixed with `indent` (default 4 spaces) so that
    the method sits correctly inside a class body.
    """
    i = indent       # 1 level (method def)
    ii = indent * 2  # 2 levels (method body)
    iii = indent * 3  # 3 levels (nested dict)
    iiii = indent * 4  # 4 levels (double-nested)

    op_id = endpoint["operationId"]
    method_name = camel_to_snake(op_id)
    http_method = endpoint["method"].upper()
    path = endpoint["path"]
    summary = endpoint.get("summary", "")

    # Collect parameters
    path_params = []
    query_params = []
    body_params = []

    for param in endpoint.get("parameters", []):
        if param["in"] == "header":
            continue  # Skip auth headers
        p = {
            "api_name": param["name"],  # Original name for API
            "name": _safe_name(param["name"]),  # Python-safe name
            "type": parse_type_hint(param["type"]),
            "required": param.get("required", False),
        }
        if param["in"] == "path":
            path_params.append(p)
        elif param["in"] == "query":
            query_params.append(p)

    # Body parameters
    body = endpoint.get("body", {})
    if body:
        for key, info in body.items():
            if isinstance(info, dict) and "type" in info:
                btype = info["type"]
                required = info.get("required", False)
                if isinstance(btype, dict):
                    for sub_key, sub_type in btype.items():
                        body_params.append({
                            "name": sub_key,
                            "type": parse_type_hint(sub_type),
                            "required": False,
                            "wrapper": key,
                        })
                else:
                    body_params.append({
                        "name": key,
                        "type": parse_type_hint(btype),
                        "required": required,
                    })

    # Build signature - p["name"] is already Python-safe
    sig_parts = ["self"]

    for p in path_params:
        sig_parts.append(f"{p['name']}: {p['type']}")

    sig_parts.append("*")

    for p in query_params:
        if p["required"]:
            sig_parts.append(f"{p['name']}: {p['type']}")
    for p in body_params:
        if p.get("required"):
            sig_parts.append(f"{_safe_name(p['name'])}: {p['type']}")

    for p in query_params:
        if not p["required"]:
            sig_parts.append(
                f"{p['name']}: {p['type']} | None = None"
            )
    for p in body_params:
        if not p.get("required"):
            sig_parts.append(
                f"{_safe_name(p['name'])}: {p['type']} | None = None"
            )

    if sig_parts[-1] == "*":
        sig_parts.pop()

    signature = ", ".join(sig_parts)

    lines = []

    # Method definition + docstring
    lines.append(f"{i}def {method_name}({signature}) -> dict:")
    lines.append(f'{ii}"""{summary}')
    lines.append("")
    lines.append(f"{ii}{http_method} {path}")
    lines.append(f'{ii}"""')

    # Path params dict - use api_name as key, Python name as value
    if path_params:
        pp_items = ", ".join(
            f'"{p["api_name"]}": {p["name"]}' for p in path_params
        )
        lines.append(f"{ii}_path_params = {{{pp_items}}}")
    else:
        lines.append(f"{ii}_path_params = None")

    # Query params dict - use api_name as key, Python name as value
    if query_params:
        qp_items = ", ".join(
            f'"{p["api_name"]}": {p["name"]}' for p in query_params
        )
        lines.append(f"{ii}_query_params = {{{qp_items}}}")
    else:
        lines.append(f"{ii}_query_params = None")

    # Body dict
    if body_params:
        wrappers = {p.get("wrapper") for p in body_params if p.get("wrapper")}
        if wrappers:
            lines.append(f"{ii}_json_body = {{")
            for p in body_params:
                if not p.get("wrapper"):
                    lines.append(
                        f'{iii}"{p["name"]}": {_safe_name(p["name"])},'
                    )
            for wrapper in sorted(wrappers):
                lines.append(f'{iii}"{wrapper}": {{')
                for p in body_params:
                    if p.get("wrapper") == wrapper:
                        lines.append(
                            f'{iiii}"{p["name"]}": '
                            f'{_safe_name(p["name"])},'
                        )
                lines.append(f"{iii}}},")
            lines.append(f"{ii}}}")
        else:
            bp_items = ", ".join(
                f'"{p["name"]}": {_safe_name(p["name"])}' for p in body_params
            )
            lines.append(f"{ii}_json_body = {{{bp_items}}}")
    else:
        lines.append(f"{ii}_json_body = None")

    # Request call
    lines.append(f"{ii}return self.request(")
    lines.append(f'{iii}"{http_method}",')
    lines.append(f'{iii}"{path}",')
    lines.append(f"{iii}path_params=_path_params,")
    lines.append(f"{iii}query_params=_query_params,")
    lines.append(f"{iii}json_body=_json_body,")
    lines.append(f"{ii})")

    return "\n".join(lines)


def _safe_name(name: str) -> str:
    """Make a parameter name Python-safe."""
    # Remove array brackets from names like "post_ids[]"
    name = name.replace("[]", "")
    # Replace hyphens/dots/spaces with underscores
    name = name.replace("-", "_").replace(".", "_").replace(" ", "_")
    # Prefix numeric names
    if name and name[0].isdigit():
        name = f"p_{name}"
    # Python keywords
    if name in ("type", "class", "from", "import", "in", "is", "not",
                "and", "or", "if", "else", "for", "with", "as",
                "return", "global", "pass", "raise", "break", "continue"):
        name = f"{name}_"
    # Empty or invalid names
    if not name or not name.isidentifier():
        name = f"param_{name}" if name else "param"
    return name


def generate_module(tag: str, endpoints: list[dict]) -> str:
    """Generate a complete Python module for a tag's endpoints."""
    module_name, class_name = TAG_MAP[tag]

    # Deduplicate by operationId
    seen: set[str] = set()
    unique_endpoints = []
    for ep in endpoints:
        if ep["operationId"] not in seen:
            seen.add(ep["operationId"])
            unique_endpoints.append(ep)

    methods = []
    for ep in unique_endpoints:
        methods.append(build_method(ep))

    methods_str = "\n\n".join(methods)

    lines = [
        f'"""Discourse API: {tag} endpoints.',
        "",
        "Auto-generated from openapi.json - do not edit manually.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Any",
        "",
        "if TYPE_CHECKING:",
        "    pass",
        "",
        "",
        f"class {class_name}:",
        f'    """API methods for {tag}.',
        "",
        "    Requires BaseClient.request() via mixin composition.",
        '    """',
        "",
        methods_str,
        "",
    ]

    return "\n".join(lines)


def update_client_imports(tags_used: list[str]) -> None:
    """Update api/client.py to import and inherit from all generated mixins."""
    client_path = API_DIR / "client.py"
    content = client_path.read_text()

    # Build import lines and mixin list
    imports = []
    mixins = []
    for tag in sorted(tags_used):
        module_name, class_name = TAG_MAP[tag]
        imports.append(
            f"from discourse_cli.api.{module_name} import {class_name}"
        )
        mixins.append(class_name)

    import_block = "\n".join(imports)
    mixin_bases = ", ".join(mixins)

    # Replace the DiscourseClient class definition
    old_class = (
        'class DiscourseClient(BaseClient):\n'
        '    """Full Discourse API client.\n'
        '\n'
        '    Composed from generated mixin classes. After running the code\n'
        '    generator, this class inherits from all API category mixins.\n'
        '    """'
    )
    new_class = (
        f'class DiscourseClient({mixin_bases}, BaseClient):\n'
        f'    """Full Discourse API client - composed from generated mixins."""'
    )

    # Add imports after the existing imports
    marker = "from discourse_cli.exceptions import DiscourseError, RateLimitError, map_http_error"
    content = content.replace(
        marker,
        f"{marker}\n\n# Generated mixin imports\n{import_block}",
    )
    content = content.replace(old_class, new_class)

    client_path.write_text(content)
    print(f"  Updated {client_path}")


def update_api_init(tags_used: list[str]) -> None:
    """Update api/__init__.py with all mixin exports."""
    init_path = API_DIR / "__init__.py"
    lines = ['"""Discourse API client modules."""\n']
    lines.append("from discourse_cli.api.client import DiscourseClient\n")
    for tag in sorted(tags_used):
        module_name, class_name = TAG_MAP[tag]
        lines.append(
            f"from discourse_cli.api.{module_name} import {class_name}\n"
        )

    all_names = ["DiscourseClient"]
    for tag in sorted(tags_used):
        _, class_name = TAG_MAP[tag]
        all_names.append(class_name)

    lines.append(f"\n__all__ = {all_names}\n")
    init_path.write_text("".join(lines))
    print(f"  Updated {init_path}")


def main() -> None:
    """Run the code generator."""
    print("Loading OpenAPI spec...")
    with OPENAPI_PATH.open() as f:
        spec = json.load(f)

    # Group endpoints by tag
    tag_endpoints: dict[str, list[dict]] = {}
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if method in ("parameters", "summary", "description"):
                continue
            tags = details.get("tags", ["Other"])
            op_id = details.get("operationId", "")
            if not op_id:
                continue

            # Extract parameters
            params = []
            for param in details.get("parameters", []):
                schema = param.get("schema", {})
                ptype = _extract_type(schema)
                params.append({
                    "name": param["name"],
                    "in": param["in"],
                    "required": param.get("required", False),
                    "type": ptype,
                })

            # Extract request body
            body = {}
            req_body = details.get("requestBody", {})
            if req_body:
                content = req_body.get("content", {})
                for content_type, content_detail in content.items():
                    schema = content_detail.get("schema", {})
                    props = schema.get("properties", {})
                    required_list = schema.get("required", [])
                    for prop_name, prop_schema in props.items():
                        ptype = _extract_type(prop_schema)
                        body[prop_name] = {
                            "type": ptype,
                            "required": prop_name in required_list,
                        }
                    break  # Only process first content type

            endpoint = {
                "path": path,
                "method": method.upper(),
                "operationId": op_id,
                "summary": details.get("summary", ""),
                "parameters": params,
                "body": body,
            }

            for tag in tags:
                if tag in TAG_MAP:
                    tag_endpoints.setdefault(tag, []).append(endpoint)

    # Generate modules
    tags_used = []
    for tag, endpoints in sorted(tag_endpoints.items()):
        module_name, class_name = TAG_MAP[tag]
        print(f"Generating {module_name}.py ({class_name}, "
              f"{len(endpoints)} endpoints)...")

        code = generate_module(tag, endpoints)
        output_path = API_DIR / f"{module_name}.py"
        output_path.write_text(code)
        tags_used.append(tag)

    # Update client.py with mixin imports
    print("\nUpdating client.py and __init__.py...")
    update_client_imports(tags_used)
    update_api_init(tags_used)

    print(f"\nDone! Generated {len(tags_used)} API modules.")


def _extract_type(schema: dict) -> str:
    """Extract a type string from an OpenAPI schema."""
    if not schema:
        return "str"

    schema_type = schema.get("type", "string")

    if schema_type == "array":
        items = schema.get("items", {})
        inner = _extract_type(items)
        return f"array<{inner}>"

    if schema_type == "object":
        props = schema.get("properties", {})
        if props:
            return {k: _extract_type(v) for k, v in props.items()}
        return "object"

    # Handle enums
    enum = schema.get("enum")
    if enum:
        return f"string({','.join(str(e) for e in enum)})"

    # Handle format
    fmt = schema.get("format")
    if fmt:
        return f"string({fmt})"

    type_map = {
        "string": "string",
        "integer": "integer",
        "boolean": "boolean",
        "number": "number",
    }
    return type_map.get(schema_type, "string")


if __name__ == "__main__":
    main()
