import json
from collections.abc import AsyncIterator

from app.api.routers.settings import get_temperature
from app.application.exceptions.llm import LLMProviderUnavailable
from app.application.interfaces.calendar_client import CalendarClient
from app.application.interfaces.drive_client import DriveClient
from app.application.interfaces.jira_client import JiraClient
from app.application.interfaces.llm_provider import LLMProvider
from app.application.tools import (
    ToolRegistry,
    execute_calendar_tool,
    execute_drive_tool,
    execute_jira_tool,
    execute_web_tool,
)
from app.domain.models import ChatRequest, ChatResponse
from app.infrastructure.llm.openai.client import OpenAIClient
from app.infrastructure.llm.openai.exceptions import OpenAIClientError
from app.infrastructure.llm.openai.mapper import OpenAIMapper


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLM provider contract.
    Supports function calling (tools) with automatic tool execution loop.
    """

    def __init__(
        self,
        client: OpenAIClient | None = None,
        mapper: OpenAIMapper | None = None,
        tool_registry: ToolRegistry | None = None,
        jira_client: JiraClient | None = None,
        calendar_client: CalendarClient | None = None,
        drive_client: DriveClient | None = None,
    ) -> None:
        self._client = client or OpenAIClient()
        self._mapper = mapper or OpenAIMapper()
        self._tool_registry = tool_registry
        self._jira_client = jira_client
        self._calendar_client = calendar_client
        self._drive_client = drive_client

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Sends a chat request to OpenAI (non-streaming).
        Handles tool calls in a loop until the model produces a final answer.
        """

        messages = self._mapper.to_openai_messages(request)
        tools = (
            self._tool_registry.tools
            if self._tool_registry and self._tool_registry.enabled
            else None
        )

        try:
            # Tool-calling loop (max 5 iterations to prevent infinite loops)
            for _ in range(5):
                completion = await self._client.chat(
                    model=request.model,
                    messages=messages,
                    tools=tools,
                    temperature=get_temperature(),
                )

                choice = completion.choices[0]

                # If no tool calls, we have the final answer
                if not choice.message.tool_calls:
                    break

                # Process tool calls
                messages.append(choice.message.model_dump())

                for tool_call in choice.message.tool_calls:
                    result = await self._execute_tool(
                        tool_call.function.name,
                        json.loads(tool_call.function.arguments),
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )

        except OpenAIClientError as exc:
            raise LLMProviderUnavailable("LLM provider is currently unavailable") from exc

        return self._mapper.to_chat_response(completion)

    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        """
        Sends a streaming chat request to OpenAI.

        Strategy: First resolve any tool calls (non-streaming),
        then stream the final response.
        """

        messages = self._mapper.to_openai_messages(request)
        tools = (
            self._tool_registry.tools
            if self._tool_registry and self._tool_registry.enabled
            else None
        )

        try:
            # First, handle potential tool calls (non-streaming)
            if tools:
                for _ in range(5):
                    completion = await self._client.chat(
                        model=request.model,
                        messages=messages,
                        tools=tools,
                        temperature=get_temperature(),
                    )

                    choice = completion.choices[0]

                    if not choice.message.tool_calls:
                        # No tool calls — stream from here
                        # Yield the content we already have
                        if choice.message.content:
                            yield choice.message.content
                        return

                    # Process tool calls
                    messages.append(choice.message.model_dump())

                    for tool_call in choice.message.tool_calls:
                        result = await self._execute_tool(
                            tool_call.function.name,
                            json.loads(tool_call.function.arguments),
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result,
                            }
                        )

                # After tool loop, stream the final response (no tools)
                async for chunk in self._client.chat_stream(
                    model=request.model,
                    messages=messages,
                ):
                    yield chunk
            else:
                # No tools — just stream directly
                async for chunk in self._client.chat_stream(
                    model=request.model,
                    messages=messages,
                ):
                    yield chunk

        except OpenAIClientError as exc:
            raise LLMProviderUnavailable("LLM provider is currently unavailable") from exc

    async def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool call and return the result."""

        if self._tool_registry and self._tool_registry.is_web_tool(tool_name):
            return await execute_web_tool(tool_name, arguments)

        if self._tool_registry and self._tool_registry.is_calendar_tool(tool_name):
            if not self._calendar_client:
                return json.dumps({"error": "Google Calendar is not configured"})
            return await execute_calendar_tool(self._calendar_client, tool_name, arguments)

        if self._tool_registry and self._tool_registry.is_drive_tool(tool_name):
            if not self._drive_client:
                return json.dumps({"error": "Google Drive is not configured"})
            return await execute_drive_tool(self._drive_client, tool_name, arguments)

        if self._tool_registry and self._tool_registry.is_jira_tool(tool_name):
            if not self._jira_client:
                return json.dumps({"error": "Jira integration is not configured"})
            return await execute_jira_tool(self._jira_client, tool_name, arguments)

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
