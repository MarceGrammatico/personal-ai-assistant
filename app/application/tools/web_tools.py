import json

import httpx
from ddgs import DDGS

WEB_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current information. "
                "Use this when you need up-to-date data, news, "
                "documentation, or any information you don't have."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": (
                "Fetch the text content of a specific URL. "
                "Use this to read articles, documentation, or "
                "web pages when you have a specific URL."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch",
                    },
                },
                "required": ["url"],
            },
        },
    },
]


async def execute_web_tool(tool_name: str, arguments: dict) -> str:
    """Execute a web tool and return results as JSON string."""

    try:
        if tool_name == "web_search":
            result = await _web_search(arguments["query"])

        elif tool_name == "web_fetch":
            result = await _web_fetch(arguments["url"])

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)


async def _web_search(query: str) -> dict:
    """
    Search the web using DuckDuckGo.
    Returns a list of results with title, url, and snippet.
    """

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8))

        formatted = [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in results
        ]

        return {
            "query": query,
            "results": formatted,
        }

    except Exception as e:
        return {
            "query": query,
            "results": [],
            "error": str(e),
        }


async def _web_fetch(url: str) -> dict:
    """
    Fetch a URL and return its text content (truncated).
    """

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        resp = await client.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            },
        )
        resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")

    if "text/html" in content_type:
        text = _extract_text_from_html(resp.text)
    else:
        text = resp.text

    # Truncate to avoid token overflow
    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[... content truncated ...]"

    return {
        "url": url,
        "content": text,
    }


def _extract_text_from_html(html: str) -> str:
    """Simple HTML to text extraction."""

    import re

    # Remove script and style tags
    text = re.sub(
        r"<(script|style)[^>]*>.*?</\1>",
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Remove tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    # Decode entities
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&nbsp;", " ")

    return text.strip()
