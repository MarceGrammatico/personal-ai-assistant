from app.domain.models import Conversation, Message, MessageRole


def test_should_create_conversation():
    conversation = Conversation(title="Sprint Planning")

    assert conversation.title == "Sprint Planning"


def test_should_start_empty():
    conversation = Conversation(title="Sprint Planning")

    assert conversation.is_empty()


def test_should_add_message():
    conversation = Conversation(title="Sprint Planning")

    conversation.add_message(Message(role=MessageRole.USER, content="Hello"))

    assert conversation.message_count() == 1


def test_should_return_last_message():
    conversation = Conversation(title="Sprint Planning")

    message = Message(role=MessageRole.USER, content="Hello")
    conversation.add_message(message)

    assert conversation.last_message() == message


def test_should_return_none_when_empty():
    conversation = Conversation(title="Sprint Planning")

    assert conversation.last_message() is None


def test_should_rename_conversation():
    conversation = Conversation(title="Old")

    conversation.rename("New")

    assert conversation.title == "New"


def test_should_update_timestamp_when_message_is_added():
    conversation = Conversation(title="Sprint")

    before = conversation.updated_at

    conversation.add_message(Message(role=MessageRole.USER, content="Hello"))

    assert conversation.updated_at >= before


def test_should_add_user_message():
    conversation = Conversation(title="Test")

    conversation.add_message_from_user("Hello")

    assert len(conversation.messages) == 1
    assert conversation.messages[0].role == MessageRole.USER
    assert conversation.messages[0].content == "Hello"


def test_should_add_assistant_message():
    conversation = Conversation(title="Test")

    conversation.add_message_from_assistant("Hi!")

    assert len(conversation.messages) == 1
    assert conversation.messages[0].role == MessageRole.ASSISTANT


def test_should_add_message_from_user():
    conversation = Conversation(title="Test")

    message = Message(role=MessageRole.USER, content="Hello")
    conversation.add_message(message)

    assert conversation.messages[0] == message


def test_should_include_system_prompt_in_llm_messages():
    conversation = Conversation(
        title="Test",
        system_prompt="You are a helper.",
    )
    conversation.add_message_from_user("Hello")

    messages = conversation.get_messages_for_llm()

    assert len(messages) == 2
    assert messages[0].role == MessageRole.SYSTEM
    assert messages[0].content == "You are a helper."
    assert messages[1].role == MessageRole.USER


def test_should_truncate_messages_preserving_system_prompt():
    conversation = Conversation(
        title="Test",
        system_prompt="System",
    )

    for i in range(10):
        conversation.add_message_from_user(f"Message {i}")

    messages = conversation.get_messages_for_llm(max_messages=3)

    # System prompt + last 3 messages
    assert len(messages) == 4
    assert messages[0].role == MessageRole.SYSTEM
    assert messages[1].content == "Message 7"


def test_should_work_without_system_prompt():
    conversation = Conversation(title="Test")
    conversation.add_message_from_user("Hello")

    messages = conversation.get_messages_for_llm()

    assert len(messages) == 1
    assert messages[0].role == MessageRole.USER
