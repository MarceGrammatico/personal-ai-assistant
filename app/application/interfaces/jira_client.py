from abc import ABC, abstractmethod


class JiraClient(ABC):
    """
    Contract for interacting with Jira.
    """

    @abstractmethod
    async def get_issue(self, issue_key: str) -> dict:
        """Get a single issue by key (e.g., 'PROJ-123')."""

    @abstractmethod
    async def search_issues(self, jql: str, max_results: int = 20) -> list[dict]:
        """Search issues using JQL."""

    @abstractmethod
    async def get_my_issues(self, max_results: int = 20) -> list[dict]:
        """Get issues assigned to the authenticated user."""

    @abstractmethod
    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str | None = None,
        issue_type: str = "Task",
    ) -> dict:
        """Create a new issue."""

    @abstractmethod
    async def add_comment(self, issue_key: str, body: str) -> dict:
        """Add a comment to an issue."""

    @abstractmethod
    async def transition_issue(self, issue_key: str, transition_name: str) -> None:
        """Transition an issue to a new status."""

    @abstractmethod
    async def get_transitions(self, issue_key: str) -> list[dict]:
        """Get available transitions for an issue."""
