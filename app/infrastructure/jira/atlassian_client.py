import httpx

from app.application.interfaces.jira_client import JiraClient
from app.core.config import settings


class AtlassianJiraClient(JiraClient):
    """
    Jira Cloud REST API client using basic auth (email + API token).

    Uses the enhanced search endpoint (GET /rest/api/3/search/jql)
    since the classic /search was removed (410 Gone) in 2025.

    Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
    """

    def __init__(self) -> None:
        self._base_url = f"https://{settings.JIRA_DOMAIN}/rest/api/3"
        self._auth = (settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._base_url,
            auth=self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=30,
        )

    async def get_issue(self, issue_key: str) -> dict:
        async with self._client() as client:
            resp = await client.get(
                f"/issue/{issue_key}",
                params={
                    "fields": ("summary,status,assignee,priority,description,issuetype"),
                },
            )
            resp.raise_for_status()
            return self._format_issue(resp.json())

    async def search_issues(self, jql: str, max_results: int = 20) -> list[dict]:
        """
        Search issues using GET /rest/api/3/search/jql
        (Enhanced JQL search endpoint).
        """

        async with self._client() as client:
            resp = await client.get(
                "/search/jql",
                params={
                    "jql": jql,
                    "maxResults": max_results,
                    "fields": ("summary,status,assignee,priority,issuetype"),
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return [self._format_issue(issue) for issue in data.get("issues", [])]

    async def get_my_issues(self, max_results: int = 20) -> list[dict]:
        jql = "assignee = currentUser() AND resolution = Unresolved ORDER BY updated DESC"
        return await self.search_issues(jql, max_results)

    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str | None = None,
        issue_type: str = "Task",
    ) -> dict:
        fields: dict = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }

        if description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }

        async with self._client() as client:
            resp = await client.post("/issue", json={"fields": fields})
            resp.raise_for_status()
            data = resp.json()
            return {
                "key": data["key"],
                "url": (f"https://{settings.JIRA_DOMAIN}/browse/{data['key']}"),
            }

    async def add_comment(self, issue_key: str, body: str) -> dict:
        comment_body = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": body}],
                    }
                ],
            }
        }

        async with self._client() as client:
            resp = await client.post(
                f"/issue/{issue_key}/comment",
                json=comment_body,
            )
            resp.raise_for_status()
            return {"id": resp.json()["id"], "issue_key": issue_key}

    async def transition_issue(self, issue_key: str, transition_name: str) -> None:
        transitions = await self.get_transitions(issue_key)

        transition_id = None
        for t in transitions:
            if t["name"].lower() == transition_name.lower():
                transition_id = t["id"]
                break

        if not transition_id:
            available = [t["name"] for t in transitions]
            raise ValueError(f"Transition '{transition_name}' not found. Available: {available}")

        async with self._client() as client:
            resp = await client.post(
                f"/issue/{issue_key}/transitions",
                json={"transition": {"id": transition_id}},
            )
            resp.raise_for_status()

    async def get_transitions(self, issue_key: str) -> list[dict]:
        async with self._client() as client:
            resp = await client.get(f"/issue/{issue_key}/transitions")
            resp.raise_for_status()
            data = resp.json()
            return [{"id": t["id"], "name": t["name"]} for t in data.get("transitions", [])]

    def _format_issue(self, raw: dict) -> dict:
        """Format raw Jira issue into a clean dict."""
        fields = raw.get("fields", {})
        return {
            "key": raw["key"],
            "summary": fields.get("summary", ""),
            "status": (fields.get("status", {}).get("name", "Unknown")),
            "assignee": ((fields.get("assignee") or {}).get("displayName", "Unassigned")),
            "priority": ((fields.get("priority") or {}).get("name", "None")),
            "type": ((fields.get("issuetype") or {}).get("name", "Unknown")),
            "url": (f"https://{settings.JIRA_DOMAIN}/browse/{raw['key']}"),
        }
