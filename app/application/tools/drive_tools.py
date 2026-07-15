import json

from app.application.interfaces.drive_client import DriveClient

DRIVE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "drive_list_files",
            "description": (
                "List files in the user's Google Drive. "
                "Returns recent files sorted by last modified."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Max files to return (default 10)",
                        "default": 10,
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "drive_read_file",
            "description": (
                "Read the content of a file from Google Drive. "
                "Works with Google Docs, Sheets (as CSV), and text files."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "The file ID from Google Drive",
                    },
                },
                "required": ["file_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "drive_create_file",
            "description": "Create a new file in Google Drive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": (
                            "File name (include extension, e.g., 'notes.txt', 'report.md')"
                        ),
                    },
                    "content": {
                        "type": "string",
                        "description": "Text content of the file",
                    },
                },
                "required": ["name", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "drive_update_file",
            "description": ("Update the content of an existing file in Google Drive."),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "The file ID to update",
                    },
                    "content": {
                        "type": "string",
                        "description": "New text content for the file",
                    },
                },
                "required": ["file_id", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "drive_delete_file",
            "description": "Delete a file from Google Drive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "The file ID to delete",
                    },
                },
                "required": ["file_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "drive_search",
            "description": "Search for files in Google Drive by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search text (file name)",
                    },
                },
                "required": ["query"],
            },
        },
    },
]


async def execute_drive_tool(
    drive_client: DriveClient,
    tool_name: str,
    arguments: dict,
) -> str:
    """Execute a Drive tool and return result as JSON string."""

    try:
        if tool_name == "drive_list_files":
            result = await drive_client.list_files(
                max_results=arguments.get("max_results", 10),
            )

        elif tool_name == "drive_read_file":
            result = await drive_client.read_file(
                file_id=arguments["file_id"],
            )

        elif tool_name == "drive_create_file":
            result = await drive_client.create_file(
                name=arguments["name"],
                content=arguments["content"],
            )

        elif tool_name == "drive_update_file":
            result = await drive_client.update_file(
                file_id=arguments["file_id"],
                content=arguments["content"],
            )

        elif tool_name == "drive_delete_file":
            await drive_client.delete_file(
                file_id=arguments["file_id"],
            )
            result = {"success": True, "message": "File deleted"}

        elif tool_name == "drive_search":
            result = await drive_client.search_files(
                query=arguments["query"],
            )

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)
