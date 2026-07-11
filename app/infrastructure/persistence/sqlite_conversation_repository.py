import sqlite3
from datetime import datetime
from pathlib import Path
from uuid import UUID

from app.application.interfaces.conversation_repository import ConversationRepository
from app.domain.models import Conversation, Message
from app.domain.models.enums import MessageRole


class SQLiteConversationRepository(ConversationRepository):
    """
    SQLite implementation of ConversationRepository.

    Persists conversations and messages to a local SQLite database.
    Suitable for single-user / single-instance deployments.
    """

    def __init__(self, db_path: str = "data/conversations.db") -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init_db(self) -> None:
        """Create tables if they don't exist."""

        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    system_prompt TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    FOREIGN KEY (conversation_id)
                        REFERENCES conversations(id)
                        ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_messages_conversation
                    ON messages(conversation_id, position);
            """)

    async def get(self, conversation_id: UUID) -> Conversation | None:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (str(conversation_id),),
            ).fetchone()

            if not row:
                return None

            messages_rows = conn.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY position ASC",
                (str(conversation_id),),
            ).fetchall()

        messages = [
            Message(
                id=UUID(msg["id"]),
                role=MessageRole(msg["role"]),
                content=msg["content"],
                created_at=datetime.fromisoformat(msg["created_at"]),
            )
            for msg in messages_rows
        ]

        return Conversation(
            id=UUID(row["id"]),
            title=row["title"],
            system_prompt=row["system_prompt"],
            messages=messages,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    async def save(self, conversation: Conversation) -> None:
        with self._get_connection() as conn:
            # Upsert conversation
            conn.execute(
                """
                INSERT INTO conversations (
                    id, title, system_prompt, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    system_prompt = excluded.system_prompt,
                    updated_at = excluded.updated_at
                """,
                (
                    str(conversation.id),
                    conversation.title,
                    conversation.system_prompt,
                    conversation.created_at.isoformat(),
                    conversation.updated_at.isoformat(),
                ),
            )

            # Replace all messages (simple approach for correctness)
            conn.execute(
                "DELETE FROM messages WHERE conversation_id = ?",
                (str(conversation.id),),
            )

            if conversation.messages:
                conn.executemany(
                    """
                    INSERT INTO messages (
                        id, conversation_id, role,
                        content, created_at, position
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            str(msg.id),
                            str(conversation.id),
                            msg.role.value,
                            msg.content,
                            msg.created_at.isoformat(),
                            idx,
                        )
                        for idx, msg in enumerate(conversation.messages)
                    ],
                )

    async def delete(self, conversation_id: UUID) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "DELETE FROM conversations WHERE id = ?",
                (str(conversation_id),),
            )

    async def list_recent(self, limit: int = 20) -> list[dict]:
        """
        List recent conversations (metadata only, no messages).
        Useful for a conversation sidebar/history.
        """

        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, created_at, updated_at,
                    (SELECT COUNT(*) FROM messages
                     WHERE conversation_id = c.id) as message_count
                FROM conversations c
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "message_count": row["message_count"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]
