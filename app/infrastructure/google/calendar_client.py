import asyncio
from datetime import UTC, datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.application.interfaces.calendar_client import CalendarClient
from app.core.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarClient(CalendarClient):
    """
    Google Calendar API client using OAuth2.

    On first run, opens a browser for authentication.
    Token is saved to disk for subsequent uses.
    """

    def __init__(self) -> None:
        self._credentials_path = Path(settings.GOOGLE_CALENDAR_CREDENTIALS_PATH)
        self._token_path = Path(settings.GOOGLE_CALENDAR_TOKEN_PATH)
        self._service = None

    def _get_service(self):
        """Get or create the Google Calendar service."""

        if self._service:
            return self._service

        creds = None

        # Load saved token
        if self._token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self._token_path), SCOPES)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self._credentials_path.exists():
                    raise FileNotFoundError(
                        f"Google credentials file not found: "
                        f"{self._credentials_path}. "
                        f"Download it from Google Cloud Console."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self._credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save token for next time
            self._token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._token_path, "w") as token:
                token.write(creds.to_json())

        self._service = build("calendar", "v3", credentials=creds)
        return self._service

    async def get_upcoming_events(self, max_results: int = 10) -> list[dict]:
        now = datetime.now(UTC).isoformat()

        def _fetch():
            service = self._get_service()
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            return events_result.get("items", [])

        events = await asyncio.to_thread(_fetch)
        return [self._format_event(e) for e in events]

    async def get_events_for_date(self, date: str, max_results: int = 20) -> list[dict]:
        time_min = f"{date}T00:00:00Z"
        time_max = f"{date}T23:59:59Z"

        def _fetch():
            service = self._get_service()
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=time_min,
                    timeMax=time_max,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            return events_result.get("items", [])

        events = await asyncio.to_thread(_fetch)
        return [self._format_event(e) for e in events]

    async def create_event(
        self,
        summary: str,
        start: str,
        end: str,
        description: str | None = None,
        location: str | None = None,
    ) -> dict:
        # Detect all-day vs timed event
        if "T" in start:
            start_body = {"dateTime": start, "timeZone": "UTC"}
            end_body = {"dateTime": end, "timeZone": "UTC"}
        else:
            start_body = {"date": start}
            end_body = {"date": end}

        event_body: dict = {
            "summary": summary,
            "start": start_body,
            "end": end_body,
        }

        if description:
            event_body["description"] = description
        if location:
            event_body["location"] = location

        def _create():
            service = self._get_service()
            return service.events().insert(calendarId="primary", body=event_body).execute()

        event = await asyncio.to_thread(_create)

        return {
            "id": event["id"],
            "summary": event.get("summary", ""),
            "url": event.get("htmlLink", ""),
        }

    async def delete_event(self, event_id: str) -> None:
        def _delete():
            service = self._get_service()
            service.events().delete(calendarId="primary", eventId=event_id).execute()

        await asyncio.to_thread(_delete)

    async def search_events(self, query: str, max_results: int = 10) -> list[dict]:
        now = datetime.now(UTC).isoformat()

        def _fetch():
            service = self._get_service()
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                    q=query,
                )
                .execute()
            )
            return events_result.get("items", [])

        events = await asyncio.to_thread(_fetch)
        return [self._format_event(e) for e in events]

    @staticmethod
    def _format_event(event: dict) -> dict:
        """Format a raw Google Calendar event."""

        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        return {
            "id": event["id"],
            "summary": event.get("summary", "(Sin título)"),
            "start": start,
            "end": end,
            "location": event.get("location", ""),
            "description": event.get("description", ""),
            "url": event.get("htmlLink", ""),
        }
