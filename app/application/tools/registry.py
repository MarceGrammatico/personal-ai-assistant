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
    ) -> None:
        self._tools: list[dict] = []

        if web_enabled:
            self._tools.extend(WEB_TOOLS)

        if jira_enabled:
            self._tools.extend(JIRA_TOOLS)

    @property
    def tools(self) -> list[dict]:
        """Return all registered tool schemas."""
        return self._tools

    @property
    def enabled(self) -> bool:
        """Whether any tools are available."""
        return len(self._tools) > 0

    def is_jira_tool(self, tool_name: str) -> bool:
        """Check if a tool name belongs to Jira."""
        return tool_name.startswith("jira_")

    def is_web_tool(self, tool_name: str) -> bool:
        """Check if a tool name belongs to web tools."""
        return tool_name.startswith("web_")
