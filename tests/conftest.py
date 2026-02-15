"""Shared test fixtures."""

import pytest

from discourse_cli.config.models import DiscourseConfig


@pytest.fixture
def config() -> DiscourseConfig:
    """Create a test config."""
    return DiscourseConfig(
        url="https://forum.example.com",
        api_key="test-api-key-1234567890",
        api_username="system",
        timeout=10,
    )
