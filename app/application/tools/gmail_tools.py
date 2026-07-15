import json

from app.application.interfaces.gmail_client import GmailClient

GMAIL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "gmail_get_recent",
            "description": ("Get recent emails from the user's Gmail inbox."),
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Max emails to return (default 5)",
                        "default": 5,
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gmail_read_email",
            "description": ("Read the full content of a specific email by its ID."),
            "parameters": {
                "type": "object",
                "properties": {
                    "message_id": {
                        "type": "string",
                        "description": "The email message ID",
                    },
                },
                "required": ["message_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gmail_send",
            "description": "Send an email from the user's Gmail account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject",
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body (plain text)",
                    },
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gmail_search",
            "description": (
                "Search emails in Gmail. Uses Gmail query syntax "
                "(e.g., 'from:john subject:meeting', 'is:unread', "
                "'after:2026/07/01')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Gmail search query",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Max results (default 5)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
    },
]


async def execute_gmail_tool(
    gmail_client: GmailClient,
    tool_name: str,
    arguments: dict,
) -> str:
    """Execute a Gmail tool and return result as JSON string."""

    try:
        if tool_name == "gmail_get_recent":
            result = await gmail_client.get_recent_emails(
                max_results=arguments.get("max_results", 5),
            )

        elif tool_name == "gmail_read_email":
            result = await gmail_client.read_email(
                message_id=arguments["message_id"],
            )

        elif tool_name == "gmail_send":
            result = await gmail_client.send_email(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"],
            )

        elif tool_name == "gmail_search":
            result = await gmail_client.search_emails(
                query=arguments["query"],
                max_results=arguments.get("max_results", 5),
            )

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)
