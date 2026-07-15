from abc import ABC, abstractmethod


class GmailClient(ABC):
    """
    Contract for interacting with an email service.
    """

    @abstractmethod
    async def get_recent_emails(
        self, max_results: int = 10, query: str | None = None
    ) -> list[dict]:
        """Get recent emails. Optional query filter."""

    @abstractmethod
    async def read_email(self, message_id: str) -> dict:
        """Read a specific email by ID. Returns full content."""

    @abstractmethod
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> dict:
        """Send an email."""

    @abstractmethod
    async def search_emails(self, query: str, max_results: int = 10) -> list[dict]:
        """Search emails using Gmail query syntax."""
