import json
import logging

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.application.dependencies import (
    get_conversation_repository,
    get_send_message_use_case,
)
from app.application.dto import (
    ChatRequestDTO,
    ChatResponseDTO,
    UsageDTO,
)
from app.application.use_cases import SendMessageUseCase

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=None)
async def chat(
    request: ChatRequestDTO,
    use_case: SendMessageUseCase = Depends(  # noqa: B008
        get_send_message_use_case,
    ),
) -> ChatResponseDTO | StreamingResponse:
    """
    Send a message to the assistant.

    - Without `stream: true`: returns JSON with the full response.
    - With `stream: true`: returns Server-Sent Events (SSE) with content chunks.
    """

    if request.stream:
        return await _handle_stream(request, use_case)

    return await _handle_sync(request, use_case)


async def _handle_sync(
    request: ChatRequestDTO,
    use_case: SendMessageUseCase,
) -> ChatResponseDTO:
    """Handle non-streaming chat request."""

    result = await use_case.execute(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    return ChatResponseDTO(
        answer=result.response.message.content,
        conversation_id=result.conversation.id,
        usage=UsageDTO(
            prompt_tokens=result.response.usage.prompt_tokens,
            completion_tokens=result.response.usage.completion_tokens,
            total_tokens=result.response.usage.total_tokens,
        ),
    )


async def _handle_stream(
    request: ChatRequestDTO,
    use_case: SendMessageUseCase,
) -> StreamingResponse:
    """Handle streaming chat request via SSE."""

    conversation, stream = await use_case.execute_stream(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    async def event_generator():
        collected_content = []

        try:
            async for chunk in stream:
                collected_content.append(chunk)
                event_data = json.dumps(
                    {
                        "type": "content",
                        "data": chunk,
                    }
                )
                yield f"data: {event_data}\n\n"

            # Save the full response to conversation history
            full_content = "".join(collected_content)
            await use_case.save_streamed_response(
                conversation=conversation,
                content=full_content,
            )

            # Send done event with metadata
            done_data = json.dumps(
                {
                    "type": "done",
                    "conversation_id": str(conversation.id),
                }
            )
            yield f"data: {done_data}\n\n"

        except Exception:
            logging.exception("Error during streaming response")
            error_data = json.dumps(
                {
                    "type": "error",
                    "data": "An error occurred while generating the response.",
                }
            )
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Conversation-ID": str(conversation.id),
        },
    )


@router.get("/conversations")
async def list_conversations(
    limit: int = 20,
    repository=Depends(get_conversation_repository),  # noqa: B008
) -> list[dict]:
    """
    List recent conversations.
    Only available when using SQLite storage.
    """

    if hasattr(repository, "list_recent"):
        return await repository.list_recent(limit=limit)

    return []


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    repository=Depends(get_conversation_repository),  # noqa: B008
) -> dict:
    """
    Delete a conversation and all its messages.
    """

    from uuid import UUID

    await repository.delete(UUID(conversation_id))

    return {"success": True}


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    repository=Depends(get_conversation_repository),  # noqa: B008
) -> dict:
    """
    Get a conversation with all its messages.
    """

    from uuid import UUID

    conversation = await repository.get(UUID(conversation_id))

    if not conversation:
        return {"error": "Conversation not found"}

    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "messages": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in conversation.messages
        ],
    }
