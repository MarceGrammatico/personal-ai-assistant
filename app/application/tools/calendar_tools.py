import json

from app.application.interfaces.calendar_client import CalendarClient

CALENDAR_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calendar_get_upcoming",
            "description": (
                "Get upcoming events from the user's Google Calendar. "
                "Returns the next events starting from now."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Max events to return (default 10)",
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
            "name": "calendar_get_events_for_date",
            "description": ("Get all events for a specific date from Google Calendar."),
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": ("Date in YYYY-MM-DD format, e.g., '2026-07-15'"),
                    },
                },
                "required": ["date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_create_event",
            "description": ("Create a new event in Google Calendar."),
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Event title",
                    },
                    "start": {
                        "type": "string",
                        "description": (
                            "Start time: 'YYYY-MM-DDTHH:MM:SS' for timed, "
                            "or 'YYYY-MM-DD' for all-day"
                        ),
                    },
                    "end": {
                        "type": "string",
                        "description": (
                            "End time: 'YYYY-MM-DDTHH:MM:SS' for timed, or 'YYYY-MM-DD' for all-day"
                        ),
                    },
                    "description": {
                        "type": "string",
                        "description": "Event description (optional)",
                    },
                    "location": {
                        "type": "string",
                        "description": "Event location (optional)",
                    },
                },
                "required": ["summary", "start", "end"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_delete_event",
            "description": "Delete an event from Google Calendar by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The event ID to delete",
                    },
                },
                "required": ["event_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_search",
            "description": ("Search for events in Google Calendar by text query."),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search text",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Max results (default 10)",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        },
    },
]


async def execute_calendar_tool(
    calendar_client: CalendarClient,
    tool_name: str,
    arguments: dict,
) -> str:
    """Execute a calendar tool and return result as JSON string."""

    try:
        if tool_name == "calendar_get_upcoming":
            result = await calendar_client.get_upcoming_events(
                max_results=arguments.get("max_results", 10),
            )

        elif tool_name == "calendar_get_events_for_date":
            result = await calendar_client.get_events_for_date(
                date=arguments["date"],
            )

        elif tool_name == "calendar_create_event":
            result = await calendar_client.create_event(
                summary=arguments["summary"],
                start=arguments["start"],
                end=arguments["end"],
                description=arguments.get("description"),
                location=arguments.get("location"),
            )

        elif tool_name == "calendar_delete_event":
            await calendar_client.delete_event(
                event_id=arguments["event_id"],
            )
            result = {"success": True, "message": "Event deleted"}

        elif tool_name == "calendar_search":
            result = await calendar_client.search_events(
                query=arguments["query"],
                max_results=arguments.get("max_results", 10),
            )

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)
