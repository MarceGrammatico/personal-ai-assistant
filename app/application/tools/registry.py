from app.application.tools.calendar_tools import CALENDAR_TOOLS
from app.application.tools.drive_tools import DRIVE_TOOLS
from app.application.tools.gmail_tools import GMAIL_TOOLS
from app.application.tools.jira_tools import JIRA_TOOLS
from app.application.tools.web_tools import WEB_TOOLS


class ToolRegistry:
    """
    Registry of available tools for the LLM.

    Collects tool schemas from all integrations and provides
    them in the format expected by OpenAI function calling.
    """

    def __init__(
        self,
        jira_enabled: bool = False,
        web_enabled: bool = True,
        calendar_enabled: bool = False,
        drive_enabled: bool = False,
        gmail_enabled: bool = False,
    ) -> None:
        self._tools: list[dict] = []

        if web_enabled:
            self._tools.extend(WEB_TOOLS)

        if jira_enabled:
            self._tools.extend(JIRA_TOOLS)

        if calendar_enabled:
            self._tools.extend(CALENDAR_TOOLS)

        if drive_enabled:
            self._tools.extend(DRIVE_TOOLS)

        if gmail_enabled:
            self._tools.extend(GMAIL_TOOLS)

    @property
    def tools(self) -> list[dict]:
        return self._tools

    @property
    def enabled(self) -> bool:
        return len(self._tools) > 0

    def is_jira_tool(self, tool_name: str) -> bool:
        return tool_name.startswith("jira_")

    def is_web_tool(self, tool_name: str) -> bool:
        return tool_name.startswith("web_")

    def is_calendar_tool(self, tool_name: str) -> bool:
        return tool_name.startswith("calendar_")

    def is_drive_tool(self, tool_name: str) -> bool:
        return tool_name.startswith("drive_")

    def is_gmail_tool(self, tool_name: str) -> bool:
        return tool_name.startswith("gmail_")
