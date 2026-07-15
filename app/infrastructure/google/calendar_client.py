import asyncio
from datetime import UTC, datetime

from googleapiclient.discovery import build

from app.application.interfaces.calendar_client import CalendarClient
from app.infrastructure.google.auth import get_google_credentials


class GoogleCalendarClient(CalendarClient):
    """
    Google Calendar API client using OAuth2.

    Uses shared authentication from app.infrastructure.google.auth.
    """

    def __init__(self) -> None:
        self._service = None

    def _get_service(self):
        """Get or create the Google Calendar service."""

        if self._service:
            return self._service

        creds = get_google_credentials()
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
