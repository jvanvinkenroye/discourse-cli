# Discourse CLI

A command-line tool for Discourse forum administration via the REST API.

## Features

- **17 command groups** covering users, topics, posts, categories, groups, tags, badges, and more
- **80+ subcommands** for comprehensive forum management
- **Profile system** to manage multiple Discourse instances (production, staging, etc.)
- **Flexible output** with automatic format detection (table for TTY, JSON for pipes)
- **Generic API access** via `discourse api` for any endpoint not covered by dedicated commands

## Quick Start

```bash
# Install
uv pip install -e .

# Configure
discourse config init

# Start using
discourse users list
discourse topics list
discourse search "welcome"
```

## Example Workflow

```bash
# Set up profiles for different instances
discourse config init --profile production
discourse config init --profile staging

# Switch default profile
discourse config use production

# Or use a specific profile per command
discourse -p staging users list

# Pipe JSON output to jq
discourse users list -o json | jq '.[].username'

# Direct API access for any endpoint
discourse api GET /site.json
```

## Next Steps

- [Installation](installation.md) -- install via uv, pip, or from source
- [Configuration](configuration.md) -- profiles, environment variables, and priority resolution
- [Output Formats](output-formats.md) -- auto, JSON, table, and piping with jq
- [Commands](commands/index.md) -- full reference for all command groups
