from abc import ABC, abstractmethod


class DriveClient(ABC):
    """
    Contract for interacting with a cloud file storage service.
    """

    @abstractmethod
    async def list_files(self, query: str | None = None, max_results: int = 20) -> list[dict]:
        """List files. Optional query filter (Google Drive query syntax)."""

    @abstractmethod
    async def read_file(self, file_id: str) -> dict:
        """Read file content. Returns metadata + text content."""

    @abstractmethod
    async def create_file(
        self,
        name: str,
        content: str,
        mime_type: str = "text/plain",
        folder_id: str | None = None,
    ) -> dict:
        """Create a new file with text content."""

    @abstractmethod
    async def update_file(self, file_id: str, content: str) -> dict:
        """Update an existing file's content."""

    @abstractmethod
    async def delete_file(self, file_id: str) -> None:
        """Delete a file by ID."""

    @abstractmethod
    async def search_files(self, query: str, max_results: int = 10) -> list[dict]:
        """Search files by name or content."""
