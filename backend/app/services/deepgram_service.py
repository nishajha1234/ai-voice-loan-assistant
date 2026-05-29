from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions
)

from app.core.config import settings
from app.utils.logger import logger

import time


class DeepgramService:

    def __init__(self):

        if not settings.DEEPGRAM_API_KEY:

            raise Exception(
                "DEEPGRAM_API_KEY missing"
            )

        config = DeepgramClientOptions(
            options={
                "keepalive": "true"
            }
        )

        self.client = DeepgramClient(
            settings.DEEPGRAM_API_KEY,
            config
        )

        self.connection = None

        self.connection_ready = False

        self.transcript_callback = None

        self.connection_started_at = None

        self.total_transcripts = 0

        self.total_final_transcripts = 0

        self.language = "multi"

    # ========================================
    # CALLBACK SETTER
    # ========================================

    def set_transcript_callback(
        self,
        callback
    ):

        self.transcript_callback = callback

    # ========================================
    # CONNECTION SETUP
    # ========================================

    async def setup_connection(
        self,
        language="multi"
    ):

        if self.connection_ready:

            logger.warning(
                "Deepgram already connected"
            )

            return True

        try:

            self.connection = (
                self.client.listen.websocket.v("1")
            )

            self.connection.on(
                LiveTranscriptionEvents.Open,
                self.on_open
            )

            self.connection.on(
                LiveTranscriptionEvents.Transcript,
                self.on_message
            )

            self.connection.on(
                LiveTranscriptionEvents.Error,
                self.on_error
            )

            self.connection.on(
                LiveTranscriptionEvents.Close,
                self.on_close
            )

            self.language = language

            options = LiveOptions(

                # Model
                model="nova-2",

                # Language
                language=self.language,

                # Audio format
                encoding="linear16",

                # Mono channel
                channels=1,

                # Browser sample rate
                sample_rate=16000,

                # Better formatting
                smart_format=True,

                # Realtime partial transcripts
                interim_results=True,

                # Auto punctuation
                punctuate=True,

                # Faster speech endpoint detection
                endpointing=500,

                # End-of-utterance timeout
                utterance_end_ms=2000,

                # Voice activity events
                vad_events=True,
            )

            logger.info(
                "Starting Deepgram websocket..."
            )

            success = self.connection.start(
                options
            )

            if not success:

                logger.error(
                    "Deepgram start returned False"
                )

                self.connection = None

                self.connection_ready = False

                return False

            self.connection_ready = True

            self.connection_started_at = (
                time.perf_counter()
            )

            logger.info(
                "Deepgram realtime connection established"
            )

            return True

        except Exception as e:

            logger.error(
                f"Deepgram setup error: {e}"
            )

            self.connection = None

            self.connection_ready = False

            return False

    # ========================================
    # STREAM AUDIO
    # ========================================

    def stream_audio(
        self,
        audio_chunk: bytes
    ):

        if not self.connection_ready:
            return

        if not self.connection:
            return

        if not audio_chunk:
            return

        try:

            self.connection.send(
                audio_chunk
            )

        except Exception as e:

            logger.error(
                f"Deepgram send error: {e}"
            )

            self.connection_ready = False

    # ========================================
    # CLOSE CONNECTION
    # ========================================

    async def close(self):

        if not self.connection:
            return

        try:

            if self.connection_ready:

                self.connection.finish()

            connection_duration = 0

            if self.connection_started_at:

                connection_duration = round(
                    time.perf_counter()
                    - self.connection_started_at,
                    2
                )

            logger.info(
                f"Deepgram connection closed "
                f"after {connection_duration}s"
            )

            logger.info(
                f"Total transcripts: "
                f"{self.total_transcripts}"
            )

            logger.info(
                f"Final transcripts: "
                f"{self.total_final_transcripts}"
            )

        except Exception as e:

            logger.error(
                f"Deepgram close error: {e}"
            )

        finally:

            self.connection = None

            self.connection_ready = False

    # ========================================
    # EVENTS
    # ========================================

    def on_open(
        self,
        *args,
        **kwargs
    ):

        logger.info(
            "Deepgram websocket opened"
        )

        self.connection_ready = True

    def on_close(
        self,
        *args,
        **kwargs
    ):

        logger.info(
            "Deepgram websocket closed"
        )

        self.connection_ready = False

    def on_error(
        self,
        *args,
        **kwargs
    ):

        logger.error(
            f"Deepgram websocket error: "
            f"{args}"
        )

        self.connection_ready = False

    # ========================================
    # TRANSCRIPT EVENT
    # ========================================

    def on_message(
        self,
        connection,
        result,
        **kwargs
    ):

        try:

            alternatives = (
                result.channel.alternatives
            )

            if not alternatives:
                return

            transcript = (
                alternatives[0].transcript
            )

            if not transcript:
                return

            self.total_transcripts += 1

            transcript_type = (
                "final"
                if result.is_final
                else "interim"
            )

            if result.is_final:

                self.total_final_transcripts += 1

            transcript_data = {

                "type": transcript_type,

                "transcript": transcript,

                "is_final": result.is_final,

                "speech_final": (
                    result.speech_final
                ),

                "transcript_received_at": (
                    time.time()
                )
            }

            logger.info(
                f"[{transcript_type.upper()}] "
                f"{transcript}"
            )

            if self.transcript_callback:

                try:

                    self.transcript_callback(
                        transcript_data
                    )

                except Exception as callback_error:

                    logger.error(
                        f"Transcript callback error: "
                        f"{callback_error}"
                    )

        except Exception as e:

            logger.error(
                f"Transcript processing error: {e}"
            )