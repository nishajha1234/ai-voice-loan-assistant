from app.db.database import SessionLocal

from app.db.models import (
    CallSession,
    TranscriptLog
)

from app.utils.logger import logger


class CRMService:

    @staticmethod
    def save_transcript(
        session_id,
        transcript,
        transcript_type,
        intent,
        state,
        ai_response
    ):

        db = SessionLocal()

        try:

            entry = TranscriptLog(

                session_id=session_id,

                transcript=transcript,

                transcript_type=transcript_type,

                detected_intent=str(intent),

                conversation_state=str(state),

                ai_response=ai_response
            )

            db.add(entry)

            db.commit()

        except Exception as e:

            logger.error(
                f"Transcript DB save error: {e}"
            )

        finally:

            db.close()

    @staticmethod
    def save_session_summary(
        session_id,
        session_manager,
        duration
    ):

        db = SessionLocal()

        try:

            session = CallSession(

                session_id=session_id,

                current_intent=str(
                    session_manager.current_intent
                ),

                current_state=str(
                    session_manager.current_state
                ),

                language=session_manager.language,

                duration=duration,

                audio_chunks=(
                    session_manager.total_audio_chunks
                ),

                final_transcripts=(
                    session_manager.total_final_transcripts
                )
            )

            db.add(session)

            db.commit()

        except Exception as e:

            logger.error(
                f"Session DB save error: {e}"
            )

        finally:

            db.close()