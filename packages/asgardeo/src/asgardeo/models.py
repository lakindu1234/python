"""Data models for Asgardeo SDK."""

from dataclasses import dataclass, field

import httpx


class AsgardeoError(Exception):
    """Base exception class for Asgardeo SDK errors."""


class AuthenticationError(AsgardeoError):
    """Raised when authentication fails."""


class TokenError(AsgardeoError):
    """Raised when token operations fail."""


class NetworkError(AsgardeoError):
    """Raised when network requests fail."""


class ValidationError(AsgardeoError):
    """Raised when input validation fails."""


@dataclass
class AsgardeoConfig:
    """Configuration for Asgardeo clients."""

    base_url: str
    client_id: str
    redirect_uri: str
    client_secret: str | None = None
    scope: str = "openid internal_login"
    session: httpx.AsyncClient = field(default_factory=httpx.AsyncClient)


@dataclass
class OAuthToken:
    """OAuth token response."""

    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str = "Bearer"
    scope: str | None = None


class FlowStatus:
    """Authentication flow status constants."""

    SUCCESS_COMPLETED = "SUCCESS_COMPLETED"
    INCOMPLETE = "INCOMPLETE"
