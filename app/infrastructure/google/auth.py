"""
Shared Google OAuth2 authentication.

Manages a single token with all required scopes
(Calendar + Drive) so the user only authenticates once.
"""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from app.core.config import settings

# All Google scopes needed by the application
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/gmail.modify",
]


def get_google_credentials() -> Credentials:
    """
    Get valid Google OAuth2 credentials.

    Loads from saved token file, refreshes if expired,
    or raises an error if no token exists (user must run
    `make setup-google` first).
    """

    token_path = Path(settings.GOOGLE_CALENDAR_TOKEN_PATH)
    Path(settings.GOOGLE_CALENDAR_CREDENTIALS_PATH)

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed token
            with open(token_path, "w") as f:
                f.write(creds.to_json())
        else:
            raise RuntimeError(
                "Google authentication required. Run 'make setup-google' to authenticate."
            )

    return creds
