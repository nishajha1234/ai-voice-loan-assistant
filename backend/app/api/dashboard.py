from fastapi import APIRouter

from sqlalchemy import func

from app.db.database import SessionLocal
from app.db.models import (
    CallSession,
    TranscriptLog
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
async def dashboard_summary():

    db = SessionLocal()

    try:

        total_calls = (
            db.query(CallSession)
            .count()
        )

        total_transcripts = (
            db.query(TranscriptLog)
            .count()
        )

        interested = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.detected_intent
                == "IntentType.INTERESTED"
            )
            .count()
        )

        callbacks = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.detected_intent
                == "IntentType.CALLBACK"
            )
            .count()
        )

        high_ticket = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.detected_intent
                == "IntentType.HIGH_TICKET"
            )
            .count()
        )

        angry = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.detected_intent
                == "IntentType.ANGRY"
            )
            .count()
        )
        conversion_count = (
            interested
            + callbacks
            + high_ticket
        )

        conversion_rate = 0

        if total_calls > 0:

            conversion_rate = round(
                (
                    conversion_count
                    / total_calls
                ) * 100,
                2
            )

        return {

            "total_calls":
                total_calls,

            "total_transcripts":
                total_transcripts,

            "interested":
                interested,

            "callbacks":
                callbacks,

            "high_ticket":
                high_ticket,

            "angry":
                angry,

            "conversion_rate":
                conversion_rate
        }

    finally:

        db.close()

@router.get("/sentiment")
async def sentiment_summary():

    db = SessionLocal()

    try:

        positive = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.sentiment
                == "POSITIVE"
            )
            .count()
        )

        neutral = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.sentiment
                == "NEUTRAL"
            )
            .count()
        )

        negative = (
            db.query(TranscriptLog)
            .filter(
                TranscriptLog.sentiment
                == "NEGATIVE"
            )
            .count()
        )

        return {

            "positive":
                positive,

            "neutral":
                neutral,

            "negative":
                negative
        }

    finally:

        db.close()        
        
@router.get("/recent-calls")
async def recent_calls():

    db = SessionLocal()

    try:

        calls = (
            db.query(CallSession)
            .order_by(
                CallSession.created_at.desc()
            )
            .limit(20)
            .all()
        )

        return [

            {
                "session_id":
                    call.session_id,

                "intent":
                    call.current_intent,

                "state":
                    call.current_state,

                "duration":
                    call.duration,

                "language":
                    call.language
            }

            for call in calls
        ]

    finally:

        db.close()  
        
@router.get("/transcripts")
async def transcripts():

    db = SessionLocal()

    try:

        logs = (
            db.query(TranscriptLog)
            .order_by(
                TranscriptLog.created_at.desc()
            )
            .limit(50)
            .all()
        )

        return [

            {
                "transcript":
                    item.transcript,

                "intent":
                    item.detected_intent,

                "state":
                    item.conversation_state,

                "created_at":
                    item.created_at
            }

            for item in logs
        ]

    finally:

        db.close()              