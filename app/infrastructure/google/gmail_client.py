import asyncio
import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from app.application.interfaces.gmail_client import GmailClient
from app.infrastructure.google.auth import get_google_credentials


class GoogleGmailClient(GmailClient):
    """
    Gmail API client using OAuth2.

    Supports reading, searching, and sending emails.
    """

    def __init__(self) -> None:
        self._service = None

    def _get_service(self):
        if self._service:
            return self._service

        creds = get_google_credentials()
        self._service = build("gmail", "v1", credentials=creds)
        return self._service

    async def get_recent_emails(
        self, max_results: int = 10, query: str | None = None
    ) -> list[dict]:
        def _fetch():
            service = self._get_service()
            q = query or "in:inbox"
            results = (
                service.users().messages().list(userId="me", q=q, maxResults=max_results).execute()
            )

            messages = results.get("messages", [])
            emails = []

            for msg_ref in messages:
                msg = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg_ref["id"],
                        format="metadata",
                        metadataHeaders=["From", "Subject", "Date"],
                    )
                    .execute()
                )
                emails.append(self._format_email_summary(msg))

            return emails

        return await asyncio.to_thread(_fetch)

    async def read_email(self, message_id: str) -> dict:
        def _fetch():
            service = self._get_service()
            msg = (
                service.users().messages().get(userId="me", id=message_id, format="full").execute()
            )
            return self._format_email_full(msg)

        return await asyncio.to_thread(_fetch)

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> dict:
        def _send():
            service = self._get_service()

            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

            sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()

            return {
                "id": sent["id"],
                "to": to,
                "subject": subject,
                "status": "sent",
            }

        return await asyncio.to_thread(_send)

    async def search_emails(self, query: str, max_results: int = 10) -> list[dict]:
        return await self.get_recent_emails(max_results=max_results, query=query)

    @staticmethod
    def _format_email_summary(msg: dict) -> dict:
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}

        return {
            "id": msg["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", "(Sin asunto)"),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
        }

    @staticmethod
    def _format_email_full(msg: dict) -> dict:
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}

        # Extract body text
        body = ""
        payload = msg.get("payload", {})

        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8")
                    break
        else:
            data = payload.get("body", {}).get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8")

        return {
            "id": msg["id"],
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "subject": headers.get("Subject", "(Sin asunto)"),
            "date": headers.get("Date", ""),
            "body": body[:5000],  # Truncate
        }
