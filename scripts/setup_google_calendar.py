#!/usr/bin/env python3
"""
Google Calendar OAuth2 Setup

Run this script once to authenticate with Google Calendar.
It opens a browser for authorization and saves the token
to data/google_token.json for the server to use.

Usage:
    uv run python scripts/setup_google_calendar.py
"""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDENTIALS_PATH = Path("config/google_credentials.json")
TOKEN_PATH = Path("data/google_token.json")


def main():
    print("🗓️  Google Calendar Setup")
    print("=" * 40)

    if not CREDENTIALS_PATH.exists():
        print(f"\n❌ Credentials file not found: {CREDENTIALS_PATH}")
        print(
            "\nTo get this file:"
            "\n1. Go to https://console.cloud.google.com/apis/credentials"
            "\n2. Create an OAuth 2.0 Client ID (Desktop app)"
            "\n3. Download the JSON"
            f"\n4. Save it as {CREDENTIALS_PATH}"
        )
        return

    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if creds and creds.valid:
        print("\n✅ Already authenticated! Token is valid.")
        print(f"   Token: {TOKEN_PATH}")
        return

    if creds and creds.expired and creds.refresh_token:
        print("\n🔄 Token expired, refreshing...")
        creds.refresh(Request())
    else:
        print("\n🌐 Opening browser for authentication...")
        print("   (If it doesn't open, copy the URL from the terminal)")

        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    print("\n✅ Authentication successful!")
    print(f"   Token saved to: {TOKEN_PATH}")
    print("\n   You can now enable Google Calendar in .env:")
    print("   GOOGLE_CALENDAR_ENABLED=true")


if __name__ == "__main__":
    main()
