"""Tests for the admin CLI commands."""

import json
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from discourse_cli.cli.main import cli
from discourse_cli.config.models import DiscourseConfig


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def mock_config():
    """Patch config loading to return a test config."""
    with patch("discourse_cli.cli.options.load_config") as mock:
        mock.return_value = DiscourseConfig(
            url="https://test.example.com",
            api_key="test-key",
        )
        yield mock


class TestAdminSuspendCommand:
    """Tests for `discourse admin suspend`."""

    def test_suspend_with_yes(
        self, runner: CliRunner, mock_config
    ) -> None:
        with patch(
            "discourse_cli.api.client.DiscourseClient.suspend_user",
            return_value={"suspension": {"suspended_till": "2026-03-01"}},
        ):
            result = runner.invoke(cli, [
                "--url", "https://test.example.com",
                "--api-key", "test-key",
                "admin", "suspend", "123",
                "--until", "2026-03-01",
                "--reason", "test",
                "--yes",
                "-o", "json",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "suspension" in data

    def test_suspend_requires_confirmation(
        self, runner: CliRunner, mock_config
    ) -> None:
        """Without --yes, prompts for confirmation."""
        with patch(
            "discourse_cli.api.client.DiscourseClient.suspend_user",
            return_value={},
        ):
            result = runner.invoke(cli, [
                "--url", "https://test.example.com",
                "--api-key", "test-key",
                "admin", "suspend", "123",
                "--until", "2026-03-01",
                "--reason", "test",
                "-o", "json",
            ], input="n\n")
        # Should abort because user said no
        assert result.exit_code != 0


class TestAdminActivateCommand:
    """Tests for `discourse admin activate`."""

    def test_activate(
        self, runner: CliRunner, mock_config
    ) -> None:
        with patch(
            "discourse_cli.api.client.DiscourseClient.activate_user",
            return_value={"success": "OK"},
        ):
            result = runner.invoke(cli, [
                "--url", "https://test.example.com",
                "--api-key", "test-key",
                "admin", "activate", "42",
                "-o", "json",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] == "OK"


class TestAdminAnonymizeCommand:
    """Tests for `discourse admin anonymize`."""

    def test_anonymize_requires_confirmation(
        self, runner: CliRunner, mock_config
    ) -> None:
        result = runner.invoke(cli, [
            "--url", "https://test.example.com",
            "--api-key", "test-key",
            "admin", "anonymize", "42",
            "-o", "json",
        ], input="n\n")
        assert result.exit_code != 0
