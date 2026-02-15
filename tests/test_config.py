"""Tests for configuration loading, models, and profile support."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from discourse_cli.config.loader import (
    get_default_profile,
    list_profiles,
    load_config,
    save_config,
    set_default_profile,
)
from discourse_cli.config.models import DiscourseConfig
from discourse_cli.exceptions import ConfigError


class TestDiscourseConfig:
    """Tests for the Pydantic config model."""

    def test_valid_config(self) -> None:
        cfg = DiscourseConfig(
            url="https://forum.example.com",
            api_key="abc123",
            api_username="system",
        )
        assert cfg.url == "https://forum.example.com"
        assert cfg.api_key == "abc123"
        assert cfg.api_username == "system"
        assert cfg.timeout == 30
        assert cfg.default_output == "auto"

    def test_url_trailing_slash_stripped(self) -> None:
        cfg = DiscourseConfig(
            url="https://forum.example.com/",
            api_key="abc123",
        )
        assert cfg.url == "https://forum.example.com"

    def test_invalid_output_format(self) -> None:
        with pytest.raises(Exception):
            DiscourseConfig(
                url="https://forum.example.com",
                api_key="abc123",
                default_output="invalid",
            )

    def test_default_username(self) -> None:
        cfg = DiscourseConfig(
            url="https://forum.example.com",
            api_key="abc123",
        )
        assert cfg.api_username == "system"


class TestLoadConfig:
    """Tests for layered config loading."""

    def test_load_from_env_vars(self) -> None:
        env = {
            "DISCOURSE_URL": "https://env.example.com",
            "DISCOURSE_API_KEY": "env-key",
            "DISCOURSE_API_USERNAME": "env-user",
        }
        with patch.dict(os.environ, env, clear=False):
            cfg = load_config()
        assert cfg.url == "https://env.example.com"
        assert cfg.api_key == "env-key"
        assert cfg.api_username == "env-user"

    def test_cli_flags_override_env(self) -> None:
        env = {
            "DISCOURSE_URL": "https://env.example.com",
            "DISCOURSE_API_KEY": "env-key",
        }
        with patch.dict(os.environ, env, clear=False):
            cfg = load_config(url="https://cli.example.com")
        assert cfg.url == "https://cli.example.com"
        assert cfg.api_key == "env-key"

    def test_missing_required_fields_raises(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "discourse_cli.config.loader._load_config_file",
                return_value={},
            ):
                with pytest.raises(ConfigError, match="Missing required"):
                    load_config()

    def test_load_from_file(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            yaml.dump({
                "url": "https://file.example.com",
                "api_key": "file-key",
                "api_username": "file-user",
            })
        )
        with patch(
            "discourse_cli.config.loader.CONFIG_FILE", config_file
        ):
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config()
        assert cfg.url == "https://file.example.com"
        assert cfg.api_key == "file-key"

    def test_env_overrides_file(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            yaml.dump({
                "url": "https://file.example.com",
                "api_key": "file-key",
            })
        )
        env = {"DISCOURSE_API_KEY": "env-key"}
        with patch(
            "discourse_cli.config.loader.CONFIG_FILE", config_file
        ):
            with patch.dict(os.environ, env, clear=True):
                cfg = load_config()
        assert cfg.url == "https://file.example.com"
        assert cfg.api_key == "env-key"


class TestSaveConfig:
    """Tests for config file saving."""

    def test_save_and_load(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "discourse-cli"
        config_file = config_dir / "config.yaml"
        with patch("discourse_cli.config.loader.CONFIG_DIR", config_dir):
            with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
                path = save_config({
                    "url": "https://saved.example.com",
                    "api_key": "saved-key",
                    "api_username": "saved-user",
                })
        assert path == config_file
        assert config_file.exists()
        data = yaml.safe_load(config_file.read_text())
        assert data["url"] == "https://saved.example.com"


# --- Profile support tests ---


def _write_config(path: Path, data: dict) -> None:
    """Helper to write a YAML config file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, default_flow_style=False))


def _profile_config(
    profiles: dict[str, dict],
    default_profile: str = "production",
) -> dict:
    """Build a profile-based config dict."""
    return {"default_profile": default_profile, "profiles": profiles}


class TestLoadConfigWithProfiles:
    """Tests for profile-aware config loading."""

    def test_load_named_profile(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config({
            "production": {
                "url": "https://prod.example.com",
                "api_key": "prod-key",
            },
            "staging": {
                "url": "https://staging.example.com",
                "api_key": "staging-key",
            },
        }))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config(profile="staging")
        assert cfg.url == "https://staging.example.com"
        assert cfg.api_key == "staging-key"

    def test_load_default_profile_from_config(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config(
            {
                "production": {
                    "url": "https://prod.example.com",
                    "api_key": "prod-key",
                },
                "staging": {
                    "url": "https://staging.example.com",
                    "api_key": "staging-key",
                },
            },
            default_profile="staging",
        ))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config()
        assert cfg.url == "https://staging.example.com"

    def test_env_profile_overrides_default(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config(
            {
                "production": {
                    "url": "https://prod.example.com",
                    "api_key": "prod-key",
                },
                "staging": {
                    "url": "https://staging.example.com",
                    "api_key": "staging-key",
                },
            },
            default_profile="production",
        ))
        env = {"DISCOURSE_PROFILE": "staging"}
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, env, clear=True):
                cfg = load_config()
        assert cfg.url == "https://staging.example.com"

    def test_explicit_profile_overrides_env(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config({
            "production": {
                "url": "https://prod.example.com",
                "api_key": "prod-key",
            },
            "staging": {
                "url": "https://staging.example.com",
                "api_key": "staging-key",
            },
        }))
        env = {"DISCOURSE_PROFILE": "staging"}
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, env, clear=True):
                cfg = load_config(profile="production")
        assert cfg.url == "https://prod.example.com"

    def test_nonexistent_profile_raises(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config({
            "production": {
                "url": "https://prod.example.com",
                "api_key": "prod-key",
            },
        }))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(ConfigError, match="not found"):
                    load_config(profile="nonexistent")

    def test_flat_config_backward_compatible(self, tmp_path: Path) -> None:
        """Flat (legacy) config still works without profiles."""
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, {
            "url": "https://legacy.example.com",
            "api_key": "legacy-key",
            "api_username": "admin",
        })
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config()
        assert cfg.url == "https://legacy.example.com"
        assert cfg.api_key == "legacy-key"
        assert cfg.api_username == "admin"

    def test_flat_config_rejects_named_profile(self, tmp_path: Path) -> None:
        """Requesting a non-default profile from flat config raises error."""
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, {
            "url": "https://legacy.example.com",
            "api_key": "legacy-key",
        })
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(ConfigError, match="flat format"):
                    load_config(profile="staging")

    def test_cli_flags_override_profile(self, tmp_path: Path) -> None:
        """CLI flags take precedence over profile values."""
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config({
            "production": {
                "url": "https://prod.example.com",
                "api_key": "prod-key",
            },
        }))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config(
                    url="https://override.example.com",
                    profile="production",
                )
        assert cfg.url == "https://override.example.com"
        assert cfg.api_key == "prod-key"


class TestSaveConfigWithProfiles:
    """Tests for saving config with profile support."""

    def test_save_with_profile(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "discourse-cli"
        config_file = config_dir / "config.yaml"
        with patch("discourse_cli.config.loader.CONFIG_DIR", config_dir):
            with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
                save_config(
                    {"url": "https://staging.example.com", "api_key": "stg-key"},
                    profile="staging",
                )
        data = yaml.safe_load(config_file.read_text())
        assert "profiles" in data
        assert data["profiles"]["staging"]["url"] == "https://staging.example.com"
        assert data["default_profile"] == "staging"

    def test_save_multiple_profiles(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "discourse-cli"
        config_file = config_dir / "config.yaml"
        with patch("discourse_cli.config.loader.CONFIG_DIR", config_dir):
            with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
                save_config(
                    {"url": "https://prod.example.com", "api_key": "prod-key"},
                    profile="production",
                )
                save_config(
                    {"url": "https://staging.example.com", "api_key": "stg-key"},
                    profile="staging",
                )
        data = yaml.safe_load(config_file.read_text())
        assert "production" in data["profiles"]
        assert "staging" in data["profiles"]
        # First profile becomes default
        assert data["default_profile"] == "production"

    def test_save_migrates_flat_to_profile(self, tmp_path: Path) -> None:
        """Saving a named profile on a flat config migrates it."""
        config_dir = tmp_path / "discourse-cli"
        config_file = config_dir / "config.yaml"
        config_dir.mkdir(parents=True)
        _write_config(config_file, {
            "url": "https://legacy.example.com",
            "api_key": "legacy-key",
        })
        with patch("discourse_cli.config.loader.CONFIG_DIR", config_dir):
            with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
                save_config(
                    {"url": "https://staging.example.com", "api_key": "stg-key"},
                    profile="staging",
                )
        data = yaml.safe_load(config_file.read_text())
        assert "profiles" in data
        # Old flat config preserved as "default"
        assert data["profiles"]["default"]["url"] == "https://legacy.example.com"
        assert data["profiles"]["staging"]["url"] == "https://staging.example.com"

    def test_save_without_profile_stays_flat(self, tmp_path: Path) -> None:
        """Saving without a profile on empty/flat config stays flat."""
        config_dir = tmp_path / "discourse-cli"
        config_file = config_dir / "config.yaml"
        with patch("discourse_cli.config.loader.CONFIG_DIR", config_dir):
            with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
                save_config({
                    "url": "https://flat.example.com",
                    "api_key": "flat-key",
                })
        data = yaml.safe_load(config_file.read_text())
        assert "profiles" not in data
        assert data["url"] == "https://flat.example.com"


class TestListProfiles:
    """Tests for list_profiles()."""

    def test_list_profiles_with_profile_config(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config({
            "production": {"url": "https://prod.example.com", "api_key": "k"},
            "staging": {"url": "https://staging.example.com", "api_key": "k"},
            "dev": {"url": "https://dev.example.com", "api_key": "k"},
        }))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            profiles = list_profiles()
        assert profiles == ["dev", "production", "staging"]

    def test_list_profiles_flat_config_returns_empty(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, {
            "url": "https://flat.example.com",
            "api_key": "key",
        })
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            profiles = list_profiles()
        assert profiles == []

    def test_list_profiles_missing_file_returns_empty(self, tmp_path: Path) -> None:
        config_file = tmp_path / "nonexistent.yaml"
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            profiles = list_profiles()
        assert profiles == []


class TestSetDefaultProfile:
    """Tests for set_default_profile()."""

    def test_set_default_profile(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "discourse-cli"
        config_file = config_dir / "config.yaml"
        config_dir.mkdir(parents=True)
        _write_config(config_file, _profile_config(
            {
                "production": {"url": "https://prod.example.com", "api_key": "k"},
                "staging": {"url": "https://staging.example.com", "api_key": "k"},
            },
            default_profile="production",
        ))
        with patch("discourse_cli.config.loader.CONFIG_DIR", config_dir):
            with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
                set_default_profile("staging")
        data = yaml.safe_load(config_file.read_text())
        assert data["default_profile"] == "staging"

    def test_set_nonexistent_profile_raises(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config({
            "production": {"url": "https://prod.example.com", "api_key": "k"},
        }))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with pytest.raises(ConfigError, match="not found"):
                set_default_profile("nonexistent")

    def test_set_default_on_flat_config_raises(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, {
            "url": "https://flat.example.com",
            "api_key": "key",
        })
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            with pytest.raises(ConfigError, match="flat format"):
                set_default_profile("production")


class TestGetDefaultProfile:
    """Tests for get_default_profile()."""

    def test_returns_default_profile(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, _profile_config(
            {"prod": {"url": "u", "api_key": "k"}},
            default_profile="prod",
        ))
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            assert get_default_profile() == "prod"

    def test_returns_none_for_flat_config(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        _write_config(config_file, {"url": "u", "api_key": "k"})
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            assert get_default_profile() is None

    def test_returns_none_for_missing_file(self, tmp_path: Path) -> None:
        config_file = tmp_path / "nonexistent.yaml"
        with patch("discourse_cli.config.loader.CONFIG_FILE", config_file):
            assert get_default_profile() is None
