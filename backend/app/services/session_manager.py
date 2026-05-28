from app.core.constants import (
    ConversationState,
    IntentType
)

from app.utils.logger import logger

import time


class SessionManager:

    MAX_HISTORY = 20

    def __init__(self):

        self.current_state = (
            ConversationState.GREETING
        )

        self.current_intent = (
            IntentType.UNKNOWN
        )

        self.transcript_history = []

        self.language = "en"

        # ====================================
        # SESSION METRICS
        # ====================================

        self.session_started_at = time.time()

        self.total_audio_chunks = 0

        self.total_final_transcripts = 0

    def add_transcript(
        self,
        transcript: str
    ):

        self.transcript_history.append(
            transcript
        )

        if (
            len(self.transcript_history)
            > self.MAX_HISTORY
        ):

            self.transcript_history.pop(0)

    def update_intent(
        self,
        intent: IntentType
    ):

        logger.info(
            f"Intent updated: "
            f"{self.current_intent} -> {intent}"
        )

        self.current_intent = intent

    def update_state(
        self,
        state: ConversationState
    ):

        logger.info(
            f"State changed: "
            f"{self.current_state} -> {state}"
        )

        self.current_state = state

    def increment_audio_chunks(self):

        self.total_audio_chunks += 1

    def increment_final_transcripts(self):

        self.total_final_transcripts += 1