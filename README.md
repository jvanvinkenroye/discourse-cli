# Discourse CLI

Command-line tool for Discourse forum administration via REST API.

## Installation

```bash
uv pip install -e .
```

## Configuration

```bash
# Interactive setup
discourse config init

# Or use environment variables
export DISCOURSE_URL=https://forum.example.com
export DISCOURSE_API_KEY=your-api-key
export DISCOURSE_API_USERNAME=system
```

## Usage

```bash
# List users
discourse users list

# Get user details
discourse users get username

# Admin operations
discourse admin suspend 123 --until 2026-03-01 --reason "violation"

# Generic API call
discourse api GET /site.json

# JSON output for piping
discourse users list -o json | jq .
```
