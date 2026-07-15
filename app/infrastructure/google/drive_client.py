import asyncio
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from app.application.interfaces.drive_client import DriveClient
from app.infrastructure.google.auth import get_google_credentials


class GoogleDriveClient(DriveClient):
    """
    Google Drive API client using OAuth2.

    Supports listing, reading, creating, updating, and deleting files.
    """

    def __init__(self) -> None:
        self._service = None

    def _get_service(self):
        """Get or create the Google Drive service."""

        if self._service:
            return self._service

        creds = get_google_credentials()
        self._service = build("drive", "v3", credentials=creds)
        return self._service

    async def list_files(self, query: str | None = None, max_results: int = 20) -> list[dict]:
        q = query or "trashed = false"

        def _fetch():
            service = self._get_service()
            results = (
                service.files()
                .list(
                    q=q,
                    pageSize=max_results,
                    fields=("files(id, name, mimeType, modifiedTime, size, webViewLink)"),
                    orderBy="modifiedTime desc",
                )
                .execute()
            )
            return results.get("files", [])

        files = await asyncio.to_thread(_fetch)
        return [self._format_file(f) for f in files]

    async def read_file(self, file_id: str) -> dict:
        def _fetch():
            service = self._get_service()

            # Get metadata
            meta = service.files().get(fileId=file_id, fields="id, name, mimeType").execute()

            mime = meta.get("mimeType", "")

            # For Google Docs/Sheets/Slides, export as plain text
            if mime == "application/vnd.google-apps.document":
                content = (
                    service.files()
                    .export(fileId=file_id, mimeType="text/plain")
                    .execute()
                    .decode("utf-8")
                )
            elif mime == "application/vnd.google-apps.spreadsheet":
                content = (
                    service.files()
                    .export(fileId=file_id, mimeType="text/csv")
                    .execute()
                    .decode("utf-8")
                )
            elif mime.startswith("text/") or mime == "application/json":
                content = service.files().get_media(fileId=file_id).execute().decode("utf-8")
            else:
                content = f"[Binary file: {mime}. Cannot display content.]"

            return {
                "id": meta["id"],
                "name": meta["name"],
                "mime_type": mime,
                "content": content[:5000],  # Truncate
            }

        return await asyncio.to_thread(_fetch)

    async def create_file(
        self,
        name: str,
        content: str,
        mime_type: str = "text/plain",
        folder_id: str | None = None,
    ) -> dict:
        def _create():
            service = self._get_service()

            metadata: dict = {"name": name}
            if folder_id:
                metadata["parents"] = [folder_id]

            media = MediaIoBaseUpload(
                io.BytesIO(content.encode("utf-8")),
                mimetype=mime_type,
            )

            file = (
                service.files()
                .create(
                    body=metadata,
                    media_body=media,
                    fields="id, name, webViewLink",
                )
                .execute()
            )

            return {
                "id": file["id"],
                "name": file["name"],
                "url": file.get("webViewLink", ""),
            }

        return await asyncio.to_thread(_create)

    async def update_file(self, file_id: str, content: str) -> dict:
        def _update():
            service = self._get_service()

            media = MediaIoBaseUpload(
                io.BytesIO(content.encode("utf-8")),
                mimetype="text/plain",
            )

            file = (
                service.files()
                .update(
                    fileId=file_id,
                    media_body=media,
                    fields="id, name, modifiedTime",
                )
                .execute()
            )

            return {
                "id": file["id"],
                "name": file["name"],
                "modified": file.get("modifiedTime", ""),
            }

        return await asyncio.to_thread(_update)

    async def delete_file(self, file_id: str) -> None:
        def _delete():
            service = self._get_service()
            service.files().delete(fileId=file_id).execute()

        await asyncio.to_thread(_delete)

    async def search_files(self, query: str, max_results: int = 10) -> list[dict]:
        q = f"name contains '{query}' and trashed = false"
        return await self.list_files(query=q, max_results=max_results)

    @staticmethod
    def _format_file(file: dict) -> dict:
        return {
            "id": file["id"],
            "name": file["name"],
            "type": file.get("mimeType", ""),
            "modified": file.get("modifiedTime", ""),
            "size": file.get("size", ""),
            "url": file.get("webViewLink", ""),
        }
