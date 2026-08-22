"""Environment-based configuration for API test runs."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True, slots=True)
class Settings:
    """Connection settings shared by the API client and tests."""

    base_url: str = "http://127.0.0.1:8000"
    request_timeout: float = 10.0

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from environment variables with local defaults."""

        defaults = cls()
        return cls(
            base_url=getenv("BASE_URL", defaults.base_url).rstrip("/"),
            request_timeout=float(getenv("REQUEST_TIMEOUT", str(defaults.request_timeout))),
        )
