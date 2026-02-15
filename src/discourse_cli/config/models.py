"""Pydantic configuration models."""

from pydantic import BaseModel, field_validator


class DiscourseConfig(BaseModel):
    """Configuration for connecting to a Discourse instance."""

    url: str
    api_key: str
    api_username: str = "system"
    timeout: int = 30
    default_output: str = "auto"

    @field_validator("url")
    @classmethod
    def normalize_url(cls, v: str) -> str:
        """Strip trailing slash from URL."""
        return v.rstrip("/")

    @field_validator("default_output")
    @classmethod
    def validate_output(cls, v: str) -> str:
        """Ensure output format is valid."""
        allowed = {"auto", "json", "table"}
        if v not in allowed:
            msg = f"default_output must be one of {allowed}"
            raise ValueError(msg)
        return v
