# Installation

## Requirements

- Python 3.11 or later
- A Discourse instance with an API key

## Install with uv (recommended)

```bash
uv pip install discourse-cli
```

## Install with pip

```bash
pip install discourse-cli
```

## Install from Source

```bash
git clone https://github.com/yourusername/discourse-cli.git
cd discourse-cli
uv pip install -e .
```

## Development Setup

```bash
git clone https://github.com/yourusername/discourse-cli.git
cd discourse-cli

# Create virtual environment and install with dev dependencies
uv venv --seed
uv sync --group dev

# Verify installation
uv run discourse --version
```

## Verify

After installation, verify that the CLI is available:

```bash
discourse --version
discourse --help
```
