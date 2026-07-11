import json

from app.application.interfaces.jira_client import JiraClient

JIRA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "jira_get_my_issues",
            "description": (
                "Get Jira issues assigned to the current user. Returns a list of open issues."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of issues to return (default 10)",
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
            "name": "jira_get_issue",
            "description": "Get details of a specific Jira issue by its key (e.g., PROJ-123).",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "The Jira issue key, e.g., 'PROJ-123'",
                    }
                },
                "required": ["issue_key"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jira_search",
            "description": (
                "Search Jira issues using JQL (Jira Query Language). Use this for complex queries."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "jql": {
                        "type": "string",
                        "description": (
                            "JQL query string, e.g., 'project = PROJ AND status = \"In Progress\"'"
                        ),
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default 10)",
                        "default": 10,
                    },
                },
                "required": ["jql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jira_create_issue",
            "description": "Create a new Jira issue in a project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_key": {
                        "type": "string",
                        "description": "The project key, e.g., 'PROJ'",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Issue title/summary",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue (optional)",
                    },
                    "issue_type": {
                        "type": "string",
                        "description": "Issue type: Task, Bug, Story, Epic (default: Task)",
                        "default": "Task",
                    },
                },
                "required": ["project_key", "summary"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jira_add_comment",
            "description": "Add a comment to an existing Jira issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "The issue key, e.g., 'PROJ-123'",
                    },
                    "body": {
                        "type": "string",
                        "description": "The comment text",
                    },
                },
                "required": ["issue_key", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jira_transition_issue",
            "description": "Move a Jira issue to a new status (e.g., 'In Progress', 'Done').",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "The issue key, e.g., 'PROJ-123'",
                    },
                    "transition_name": {
                        "type": "string",
                        "description": "Target status name, e.g., 'In Progress', 'Done'",
                    },
                },
                "required": ["issue_key", "transition_name"],
            },
        },
    },
]


async def execute_jira_tool(
    jira_client: JiraClient,
    tool_name: str,
    arguments: dict,
) -> str:
    """
    Execute a Jira tool call and return the result as a JSON string.
    """

    try:
        if tool_name == "jira_get_my_issues":
            result = await jira_client.get_my_issues(
                max_results=arguments.get("max_results", 10),
            )

        elif tool_name == "jira_get_issue":
            result = await jira_client.get_issue(
                issue_key=arguments["issue_key"],
            )

        elif tool_name == "jira_search":
            result = await jira_client.search_issues(
                jql=arguments["jql"],
                max_results=arguments.get("max_results", 10),
            )

        elif tool_name == "jira_create_issue":
            result = await jira_client.create_issue(
                project_key=arguments["project_key"],
                summary=arguments["summary"],
                description=arguments.get("description"),
                issue_type=arguments.get("issue_type", "Task"),
            )

        elif tool_name == "jira_add_comment":
            result = await jira_client.add_comment(
                issue_key=arguments["issue_key"],
                body=arguments["body"],
            )

        elif tool_name == "jira_transition_issue":
            await jira_client.transition_issue(
                issue_key=arguments["issue_key"],
                transition_name=arguments["transition_name"],
            )
            result = {
                "success": True,
                "message": (
                    f"Issue {arguments['issue_key']} transitioned "
                    f"to '{arguments['transition_name']}'"
                ),
            }
        else:
            result = {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)
