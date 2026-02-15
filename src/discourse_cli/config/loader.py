"""Layered configuration resolution with profile support.

Priority: CLI flags > environment variables > config file (profile).

Config format supports both flat (legacy) and profile-based layouts:

  Flat (legacy):
    url: https://host.example.com
    api_key: abc...

  Profile-based:
    default_profile: production
    profiles:
      production:
        url: https://host.example.com
        api_key: abc...
      staging:
        url: https://staging.example.com
        api_key: def...

Profile resolution order:
  --profile flag > DISCOURSE_PROFILE env > default_profile in config > "default"
"""

import os
from pathlib import Path
from typing import Any

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

# Keys that belong to profile data (not top-level meta keys)
_PROFILE_KEYS = {"url", "api_key", "api_username", "timeout", "default_output"}


def _load_raw_config() -> dict[str, Any]:
    """Load the raw YAML config file as a dict."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        with CONFIG_FILE.open() as f:
            data = yaml.safe_load(f) or {}
        return data
    except (yaml.YAMLError, OSError) as e:
        raise ConfigError(f"Failed to read config file: {e}") from e


def _is_profile_config(data: dict[str, Any]) -> bool:
    """Check whether the config uses the profile-based format."""
    return "profiles" in data


def _resolve_profile_name(
    profile: str | None,
    data: dict[str, Any],
) -> str:
    """Determine which profile to use.

    Resolution order:
      1. Explicit profile argument (from --profile flag)
      2. DISCOURSE_PROFILE environment variable
      3. default_profile key in config file
      4. "default" as final fallback
    """
    if profile:
        return profile
    env_profile = os.environ.get("DISCOURSE_PROFILE")
    if env_profile:
        return env_profile
    if "default_profile" in data:
        return str(data["default_profile"])
    return "default"


def _load_config_file(profile: str | None = None) -> dict[str, str]:
    """Load configuration for a specific profile from the YAML config file.

    Supports both flat (legacy) and profile-based config formats.
    Flat configs are treated as the "default" profile.
    """
    data = _load_raw_config()
    if not data:
        return {}

    if _is_profile_config(data):
        profile_name = _resolve_profile_name(profile, data)
        profiles = data.get("profiles", {})
        if profile_name not in profiles:
            available = ", ".join(sorted(profiles.keys())) or "(none)"
            raise ConfigError(
                f"Profile '{profile_name}' not found. "
                f"Available profiles: {available}"
            )
        profile_data = profiles[profile_name]
        return {k: str(v) for k, v in profile_data.items()}

    # Flat (legacy) config - only use if requesting "default" or no specific profile
    resolved = _resolve_profile_name(profile, data)
    if resolved != "default":
        raise ConfigError(
            f"Profile '{resolved}' not found. "
            f"Config file uses flat format with no profiles defined."
        )
    return {k: str(v) for k, v in data.items() if k in _PROFILE_KEYS}


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
    profile: str | None = None,
    **cli_overrides: str | None,
) -> DiscourseConfig:
    """Build config from layered sources: CLI flags > env vars > file.

    Args:
        url: Discourse instance URL (CLI flag).
        api_key: API key (CLI flag).
        api_username: API username (CLI flag).
        profile: Named profile to load from config file.
        **cli_overrides: Additional CLI flag overrides.

    Returns:
        Resolved DiscourseConfig.

    Raises:
        ConfigError: If required fields are missing or profile not found.
    """
    # Layer 1: config file (lowest priority)
    merged = _load_config_file(profile=profile)

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


def save_config(
    config: dict[str, str],
    profile: str | None = None,
) -> Path:
    """Save configuration to the YAML config file.

    When profile is specified, writes under profiles.<name>.
    When profile is None and file already uses profile format,
    writes under profiles.default.

    Args:
        config: Configuration key-value pairs to save.
        profile: Profile name to save under. None uses "default".

    Returns:
        Path to the saved config file.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    existing = _load_raw_config()

    if profile or _is_profile_config(existing):
        # Profile-based format
        profile_name = profile or "default"
        if not _is_profile_config(existing):
            # Migrate: wrap existing flat config as "default" profile
            flat_data = {k: v for k, v in existing.items() if k in _PROFILE_KEYS}
            if flat_data:
                existing = {
                    "default_profile": "default",
                    "profiles": {"default": flat_data},
                }
            else:
                existing = {"profiles": {}}
        if "profiles" not in existing:
            existing["profiles"] = {}
        existing["profiles"][profile_name] = config
        # Set default_profile if not yet set
        if "default_profile" not in existing:
            existing["default_profile"] = profile_name
        with CONFIG_FILE.open("w") as f:
            yaml.dump(existing, f, default_flow_style=False)
    else:
        # Flat format (no profile specified, no existing profiles)
        with CONFIG_FILE.open("w") as f:
            yaml.dump(config, f, default_flow_style=False)

    return CONFIG_FILE


def list_profiles() -> list[str]:
    """Return all profile names from the config file.

    Returns empty list for flat configs or missing files.
    """
    data = _load_raw_config()
    if not _is_profile_config(data):
        # Flat config has no named profiles
        return []
    profiles = data.get("profiles", {})
    return sorted(profiles.keys())


def get_default_profile() -> str | None:
    """Return the default profile name, or None if not set."""
    data = _load_raw_config()
    return data.get("default_profile")


def set_default_profile(name: str) -> None:
    """Set the default_profile in the config file.

    Raises:
        ConfigError: If the profile doesn't exist.
    """
    data = _load_raw_config()

    if _is_profile_config(data):
        profiles = data.get("profiles", {})
        if name not in profiles:
            available = ", ".join(sorted(profiles.keys())) or "(none)"
            raise ConfigError(
                f"Profile '{name}' not found. Available profiles: {available}"
            )
        data["default_profile"] = name
    else:
        raise ConfigError(
            "Cannot set default profile: config file uses flat format. "
            "Create a profile first with 'discourse config init --profile <name>'."
        )

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w") as f:
        yaml.dump(data, f, default_flow_style=False)
