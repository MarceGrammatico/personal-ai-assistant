from abc import ABC, abstractmethod


class CalendarClient(ABC):
    """
    Contract for interacting with a calendar service.
    """

    @abstractmethod
    async def get_upcoming_events(self, max_results: int = 10) -> list[dict]:
        """Get upcoming events from today."""

    @abstractmethod
    async def get_events_for_date(self, date: str, max_results: int = 20) -> list[dict]:
        """Get events for a specific date (YYYY-MM-DD)."""

    @abstractmethod
    async def create_event(
        self,
        summary: str,
        start: str,
        end: str,
        description: str | None = None,
        location: str | None = None,
    ) -> dict:
        """
        Create a calendar event.
        start/end format: 'YYYY-MM-DDTHH:MM:SS' or 'YYYY-MM-DD' for all-day.
        """

    @abstractmethod
    async def delete_event(self, event_id: str) -> None:
        """Delete an event by ID."""

    @abstractmethod
    async def search_events(self, query: str, max_results: int = 10) -> list[dict]:
        """Search events by text query."""
