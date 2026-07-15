import asyncio

from googleapiclient.discovery import build

from app.application.interfaces.sheets_client import SheetsClient
from app.infrastructure.google.auth import get_google_credentials


class GoogleSheetsClient(SheetsClient):
    """
    Google Sheets API client using OAuth2.

    Supports reading, writing, appending, and creating spreadsheets.
    """

    def __init__(self) -> None:
        self._service = None

    def _get_service(self):
        if self._service:
            return self._service

        creds = get_google_credentials()
        self._service = build("sheets", "v4", credentials=creds)
        return self._service

    async def read_range(self, spreadsheet_id: str, range: str) -> dict:
        def _fetch():
            service = self._get_service()
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range)
                .execute()
            )
            return {
                "range": result.get("range", ""),
                "values": result.get("values", []),
            }

        return await asyncio.to_thread(_fetch)

    async def write_range(self, spreadsheet_id: str, range: str, values: list[list]) -> dict:
        def _write():
            service = self._get_service()
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range,
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            return {
                "updated_range": result.get("updatedRange", ""),
                "updated_cells": result.get("updatedCells", 0),
            }

        return await asyncio.to_thread(_write)

    async def append_rows(self, spreadsheet_id: str, range: str, values: list[list]) -> dict:
        def _append():
            service = self._get_service()
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range,
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body=body,
                )
                .execute()
            )
            updates = result.get("updates", {})
            return {
                "updated_range": updates.get("updatedRange", ""),
                "updated_rows": updates.get("updatedRows", 0),
            }

        return await asyncio.to_thread(_append)

    async def create_spreadsheet(self, title: str) -> dict:
        def _create():
            service = self._get_service()
            body = {"properties": {"title": title}}
            result = (
                service.spreadsheets()
                .create(body=body, fields="spreadsheetId,spreadsheetUrl")
                .execute()
            )
            return {
                "id": result["spreadsheetId"],
                "url": result["spreadsheetUrl"],
                "title": title,
            }

        return await asyncio.to_thread(_create)

    async def list_sheets(self, spreadsheet_id: str) -> list[dict]:
        def _fetch():
            service = self._get_service()
            result = (
                service.spreadsheets()
                .get(spreadsheetId=spreadsheet_id, fields="sheets.properties")
                .execute()
            )
            return [
                {
                    "id": s["properties"]["sheetId"],
                    "title": s["properties"]["title"],
                    "index": s["properties"]["index"],
                }
                for s in result.get("sheets", [])
            ]

        return await asyncio.to_thread(_fetch)
