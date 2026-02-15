"""Configuration management for Discourse CLI."""

from discourse_cli.config.loader import load_config
from discourse_cli.config.models import DiscourseConfig

__all__ = ["DiscourseConfig", "load_config"]
