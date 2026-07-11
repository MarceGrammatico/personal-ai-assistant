"""
Tool definitions for OpenAI function calling.

Each tool has:
- A schema (OpenAI tool format)
- An execute function that performs the actual action
"""

from app.application.tools.jira_tools import JIRA_TOOLS, execute_jira_tool
from app.application.tools.registry import ToolRegistry
from app.application.tools.web_tools import WEB_TOOLS, execute_web_tool

__all__ = [
    "JIRA_TOOLS",
    "ToolRegistry",
    "WEB_TOOLS",
    "execute_jira_tool",
    "execute_web_tool",
]
