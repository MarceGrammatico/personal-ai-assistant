from abc import ABC, abstractmethod


class SheetsClient(ABC):
    """
    Contract for interacting with a spreadsheet service.
    """

    @abstractmethod
    async def read_range(self, spreadsheet_id: str, range: str) -> dict:
        """Read a range of cells (e.g., 'Sheet1!A1:D10')."""

    @abstractmethod
    async def write_range(self, spreadsheet_id: str, range: str, values: list[list]) -> dict:
        """Write values to a range of cells."""

    @abstractmethod
    async def append_rows(self, spreadsheet_id: str, range: str, values: list[list]) -> dict:
        """Append rows after the last row with data."""

    @abstractmethod
    async def create_spreadsheet(self, title: str) -> dict:
        """Create a new spreadsheet."""

    @abstractmethod
    async def list_sheets(self, spreadsheet_id: str) -> list[dict]:
        """List all sheets (tabs) in a spreadsheet."""
