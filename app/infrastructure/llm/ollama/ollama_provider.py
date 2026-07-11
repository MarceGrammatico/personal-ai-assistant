import json
from collections.abc import AsyncIterator

from app.application.exceptions.llm import LLMProviderUnavailable
from app.application.interfaces.jira_client import JiraClient
from app.application.interfaces.llm_provider import LLMProvider
from app.application.tools import (
    ToolRegistry,
    execute_jira_tool,
    execute_web_tool,
)
from app.core.config import settings
from app.domain.models import (
    ChatRequest,
    ChatResponse,
    Message,
    MessageRole,
    Usage,
)
from app.infrastructure.llm.ollama.client import OllamaClient


class OllamaProvider(LLMProvider):
    """
    Ollama implementation of the LLM provider contract.

    Supports local models (LLaMA, Mistral, Qwen, etc.)
    running via Ollama with optional tool calling.
    """

    def __init__(
        self,
        client: OllamaClient | None = None,
        tool_registry: ToolRegistry | None = None,
        jira_client: JiraClient | None = None,
    ) -> None:
        self._client = client or OllamaClient()
        self._tool_registry = tool_registry
        self._jira_client = jira_client

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Sends a chat request to Ollama (non-streaming).
        Handles tool calls in a loop.
        """

        messages = self._build_messages(request)
        tools = self._get_tools()

        try:
            for _ in range(5):
                response = await self._client.chat(
                    model=settings.OLLAMA_MODEL,
                    messages=messages,
                    tools=tools,
                )

                msg = response.get("message", {})

                # If no tool calls, we have the final answer
                tool_calls = msg.get("tool_calls")
                if not tool_calls:
                    break

                # Process tool calls
                messages.append(msg)

                for tool_call in tool_calls:
                    func = tool_call.get("function", {})
                    result = await self._execute_tool(
                        func.get("name", ""),
                        func.get("arguments", {}),
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "content": result,
                        }
                    )

        except Exception as exc:
            raise LLMProviderUnavailable(f"Ollama is not available: {exc}") from exc

        content = response.get("message", {}).get("content", "")

        return ChatResponse(
            message=Message(
                role=MessageRole.ASSISTANT,
                content=content or "No response generated.",
            ),
            usage=self._extract_usage(response),
        )

    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        """
        Sends a streaming chat request to Ollama.

        Strategy: resolve tool calls first (non-streaming),
        then stream the final response.
        """

        messages = self._build_messages(request)
        tools = self._get_tools()

        try:
            # Handle tool calls first (non-streaming)
            if tools:
                for _ in range(5):
                    response = await self._client.chat(
                        model=settings.OLLAMA_MODEL,
                        messages=messages,
                        tools=tools,
                    )

                    msg = response.get("message", {})
                    tool_calls = msg.get("tool_calls")

                    if not tool_calls:
                        # No more tool calls — yield content
                        content = msg.get("content", "")
                        if content:
                            yield content
                        return

                    messages.append(msg)

                    for tool_call in tool_calls:
                        func = tool_call.get("function", {})
                        result = await self._execute_tool(
                            func.get("name", ""),
                            func.get("arguments", {}),
                        )
                        messages.append(
                            {
                                "role": "tool",
                                "content": result,
                            }
                        )

                # After tool loop, stream final response
                async for chunk in self._client.chat_stream(
                    model=settings.OLLAMA_MODEL,
                    messages=messages,
                ):
                    yield chunk
            else:
                # No tools, stream directly
                async for chunk in self._client.chat_stream(
                    model=settings.OLLAMA_MODEL,
                    messages=messages,
                ):
                    yield chunk

        except Exception as exc:
            raise LLMProviderUnavailable(f"Ollama is not available: {exc}") from exc

    def _build_messages(self, request: ChatRequest) -> list[dict]:
        """Convert domain messages to Ollama format."""

        messages = request.conversation.get_messages_for_llm(
            max_messages=settings.MAX_CONVERSATION_MESSAGES,
        )

        return [{"role": msg.role.value, "content": msg.content} for msg in messages]

    def _get_tools(self) -> list[dict] | None:
        """Get tool definitions if available."""

        if self._tool_registry and self._tool_registry.enabled:
            return self._tool_registry.tools
        return None

    async def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool call and return the result."""

        if self._tool_registry and self._tool_registry.is_web_tool(tool_name):
            return await execute_web_tool(tool_name, arguments)

        if self._tool_registry and self._tool_registry.is_jira_tool(tool_name):
            if not self._jira_client:
                return json.dumps({"error": "Jira integration is not configured"})
            return await execute_jira_tool(self._jira_client, tool_name, arguments)

        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    @staticmethod
    def _extract_usage(response: dict) -> Usage:
        """Extract token usage from Ollama response."""

        prompt_tokens = response.get("prompt_eval_count", 0)
        completion_tokens = response.get("eval_count", 0)

        return Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
