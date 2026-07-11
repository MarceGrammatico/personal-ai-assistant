def test_chat_endpoint(client):
    response = client.post(
        "/chat",
        json={"message": "Hello"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Hello! I am a fake assistant."
    assert "conversation_id" in data


def test_chat_should_continue_conversation(client):
    # First message
    response1 = client.post(
        "/chat",
        json={"message": "Hello"},
    )

    assert response1.status_code == 200
    conversation_id = response1.json()["conversation_id"]

    # Second message in same conversation
    response2 = client.post(
        "/chat",
        json={
            "message": "How are you?",
            "conversation_id": conversation_id,
        },
    )

    assert response2.status_code == 200
    assert response2.json()["conversation_id"] == conversation_id


def test_chat_stream_endpoint(client):
    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "stream": True,
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    # Collect SSE events
    events = []
    for line in response.text.strip().split("\n"):
        if line.startswith("data: "):
            events.append(line[6:])

    assert len(events) > 0

    # Last event should be "done"
    import json

    last_event = json.loads(events[-1])
    assert last_event["type"] == "done"
    assert "conversation_id" in last_event
