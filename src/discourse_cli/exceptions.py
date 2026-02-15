"""Exception hierarchy for Discourse API errors."""


class DiscourseError(Exception):
    """Base exception for all Discourse CLI errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(DiscourseError):
    """Raised when API authentication fails (401/403)."""


class NotFoundError(DiscourseError):
    """Raised when a resource is not found (404)."""


class ValidationError(DiscourseError):
    """Raised when the API rejects input (422)."""


class RateLimitError(DiscourseError):
    """Raised when the API rate limit is hit (429)."""

    def __init__(
        self, message: str, retry_after: int | None = None
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=429)


class ServerError(DiscourseError):
    """Raised for server-side errors (5xx)."""


class ConfigError(DiscourseError):
    """Raised for configuration issues."""


def map_http_error(status_code: int, message: str) -> DiscourseError:
    """Map an HTTP status code to the appropriate exception."""
    error_map: dict[int, type[DiscourseError]] = {
        401: AuthenticationError,
        403: AuthenticationError,
        404: NotFoundError,
        422: ValidationError,
        429: RateLimitError,
    }
    error_cls = error_map.get(status_code)
    if error_cls:
        return error_cls(message, status_code=status_code)
    if 500 <= status_code < 600:
        return ServerError(message, status_code=status_code)
    return DiscourseError(message, status_code=status_code)
