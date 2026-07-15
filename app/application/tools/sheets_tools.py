import json

from app.application.interfaces.sheets_client import SheetsClient

SHEETS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "sheets_read_range",
            "description": (
                "Read data from a Google Sheets spreadsheet. "
                "Returns cell values for the specified range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": ("The spreadsheet ID (from the URL)"),
                    },
                    "range": {
                        "type": "string",
                        "description": ("Cell range, e.g., 'Sheet1!A1:D10' or 'A1:Z' for all data"),
                    },
                },
                "required": ["spreadsheet_id", "range"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sheets_write_range",
            "description": (
                "Write data to a Google Sheets spreadsheet. Overwrites existing data in the range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The spreadsheet ID",
                    },
                    "range": {
                        "type": "string",
                        "description": ("Target range, e.g., 'Sheet1!A1'"),
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "description": (
                            "2D array of values (rows x columns), "
                            "e.g., [['Name','Age'],['John','30']]"
                        ),
                    },
                },
                "required": ["spreadsheet_id", "range", "values"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sheets_append_rows",
            "description": ("Append rows to the end of data in a Google Sheet."),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The spreadsheet ID",
                    },
                    "range": {
                        "type": "string",
                        "description": ("Sheet name or range, e.g., 'Sheet1'"),
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "description": ("Rows to append, e.g., [['John','30'],['Jane','25']]"),
                    },
                },
                "required": ["spreadsheet_id", "range", "values"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sheets_create",
            "description": "Create a new Google Sheets spreadsheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Name for the new spreadsheet",
                    },
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sheets_list_sheets",
            "description": ("List all sheets (tabs) in a Google Sheets spreadsheet."),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The spreadsheet ID",
                    },
                },
                "required": ["spreadsheet_id"],
            },
        },
    },
]


async def execute_sheets_tool(
    sheets_client: SheetsClient,
    tool_name: str,
    arguments: dict,
) -> str:
    """Execute a Sheets tool and return result as JSON string."""

    try:
        if tool_name == "sheets_read_range":
            result = await sheets_client.read_range(
                spreadsheet_id=arguments["spreadsheet_id"],
                range=arguments["range"],
            )

        elif tool_name == "sheets_write_range":
            result = await sheets_client.write_range(
                spreadsheet_id=arguments["spreadsheet_id"],
                range=arguments["range"],
                values=arguments["values"],
            )

        elif tool_name == "sheets_append_rows":
            result = await sheets_client.append_rows(
                spreadsheet_id=arguments["spreadsheet_id"],
                range=arguments["range"],
                values=arguments["values"],
            )

        elif tool_name == "sheets_create":
            result = await sheets_client.create_spreadsheet(
                title=arguments["title"],
            )

        elif tool_name == "sheets_list_sheets":
            result = await sheets_client.list_sheets(
                spreadsheet_id=arguments["spreadsheet_id"],
            )

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)
