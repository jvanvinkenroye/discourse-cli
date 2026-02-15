"""Layered configuration resolution.

Priority: CLI flags > environment variables > config file.
"""

import os
from pathlib import Path

import yaml
from platformdirs import user_config_dir

from discourse_cli.config.models import DiscourseConfig
from discourse_cli.exceptions import ConfigError

CONFIG_DIR = Path(user_config_dir("discourse-cli"))
CONFIG_FILE = CONFIG_DIR / "config.yaml"

# Mapping from config keys to environment variable names
ENV_MAP: dict[str, str] = {
    "url": "DISCOURSE_URL",
    "api_key": "DISCOURSE_API_KEY",
    "api_username": "DISCOURSE_API_USERNAME",
    "timeout": "DISCOURSE_TIMEOUT",
    "default_output": "DISCOURSE_DEFAULT_OUTPUT",
}


def _load_config_file() -> dict[str, str]:
    """Load configuration from the YAML config file."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        with CONFIG_FILE.open() as f:
            data = yaml.safe_load(f) or {}
        return {k: str(v) for k, v in data.items()}
    except (yaml.YAMLError, OSError) as e:
        raise ConfigError(f"Failed to read config file: {e}") from e


def _load_env_vars() -> dict[str, str]:
    """Load configuration from environment variables."""
    result: dict[str, str] = {}
    for key, env_var in ENV_MAP.items():
        value = os.environ.get(env_var)
        if value is not None:
            result[key] = value
    return result


def load_config(
    url: str | None = None,
    api_key: str | None = None,
    api_username: str | None = None,
    **cli_overrides: str | None,
) -> DiscourseConfig:
    """Build config from layered sources: CLI flags > env vars > file.

    Args:
        url: Discourse instance URL (CLI flag).
        api_key: API key (CLI flag).
        api_username: API username (CLI flag).
        **cli_overrides: Additional CLI flag overrides.

    Returns:
        Resolved DiscourseConfig.

    Raises:
        ConfigError: If required fields are missing.
    """
    # Layer 1: config file (lowest priority)
    merged = _load_config_file()

    # Layer 2: environment variables
    merged.update(_load_env_vars())

    # Layer 3: CLI flags (highest priority)
    cli_flags = {"url": url, "api_key": api_key, "api_username": api_username}
    cli_flags.update(cli_overrides)
    for key, value in cli_flags.items():
        if value is not None:
            merged[key] = value

    # Validate required fields
    missing = [k for k in ("url", "api_key") if not merged.get(k)]
    if missing:
        raise ConfigError(
            f"Missing required config: {', '.join(missing)}. "
            f"Set via CLI flags, env vars ({', '.join(ENV_MAP[k] for k in missing)}), "
            f"or config file ({CONFIG_FILE})."
        )

    try:
        return DiscourseConfig(**merged)
    except Exception as e:
        raise ConfigError(f"Invalid configuration: {e}") from e


def save_config(config: dict[str, str]) -> Path:
    """Save configuration to the YAML config file.

    Returns:
        Path to the saved config file.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w") as f:
        yaml.dump(config, f, default_flow_style=False)
    return CONFIG_FILE
