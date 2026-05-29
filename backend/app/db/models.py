from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from datetime import datetime

from app.db.database import Base


class CallSession(Base):

    __tablename__ = "call_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String,
        unique=True
    )

    current_intent = Column(String)

    current_state = Column(String)

    language = Column(String)

    duration = Column(Float)

    audio_chunks = Column(Integer)

    final_transcripts = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class TranscriptLog(Base):

    __tablename__ = "transcript_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(String)

    transcript = Column(Text)

    transcript_type = Column(String)

    detected_intent = Column(String)

    conversation_state = Column(String)

    ai_response = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )