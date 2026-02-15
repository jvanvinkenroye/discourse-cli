"""Tests for configuration loading and models."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from discourse_cli.config.loader import load_config, save_config
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
