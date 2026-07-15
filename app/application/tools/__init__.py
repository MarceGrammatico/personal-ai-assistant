"""
Tool definitions for OpenAI function calling.

Each tool has:
- A schema (OpenAI tool format)
- An execute function that performs the actual action
"""

from app.application.tools.calendar_tools import (
    CALENDAR_TOOLS,
    execute_calendar_tool,
)
from app.application.tools.drive_tools import (
    DRIVE_TOOLS,
    execute_drive_tool,
)
from app.application.tools.jira_tools import JIRA_TOOLS, execute_jira_tool
from app.application.tools.registry import ToolRegistry
from app.application.tools.web_tools import WEB_TOOLS, execute_web_tool

__all__ = [
    "CALENDAR_TOOLS",
    "DRIVE_TOOLS",
    "JIRA_TOOLS",
    "ToolRegistry",
    "WEB_TOOLS",
    "execute_calendar_tool",
    "execute_drive_tool",
    "execute_jira_tool",
    "execute_web_tool",
]
