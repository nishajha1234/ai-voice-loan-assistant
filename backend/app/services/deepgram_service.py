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

        self.transcript_callback = None

        self.connection_started_at = None

        self.total_transcripts = 0

        self.total_final_transcripts = 0
        
        self.language = "multi"

    def set_transcript_callback(
        self,
        callback
    ):

        self.transcript_callback = callback

    async def setup_connection(
    self,
    language="multi"
):

        if self.connection:
            logger.warning(
                "Deepgram connection already exists"
            )
            return

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

                # Realtime multilingual model
                model="nova-2",

                # Hindi + English auto-detection
                language=self.language,

                # Browser PCM format
                encoding="linear16",

                # Mono audio
                channels=1,

                # Browser sample rate
                sample_rate=16000,

                # Better formatting
                smart_format=True,

                # Realtime partial transcripts
                interim_results=True,

                # Auto punctuation
                punctuate=True,

                # Fast endpointing
                endpointing=300,
            )

            self.connection.start(options)

            self.connection_started_at = (
                time.perf_counter()
            )

            logger.info(
                "Deepgram realtime connection established"
            )

        except Exception as e:

            logger.error(
                f"Deepgram setup error: {e}"
            )

            raise

    def stream_audio(
        self,
        audio_chunk: bytes
    ):

        if not self.connection:
            return

        if not audio_chunk:
            return

        try:

            self.connection.send(audio_chunk)

        except Exception as e:

            logger.error(
                f"Deepgram send error: {e}"
            )

    async def close(self):

        if not self.connection:
            return

        try:

            self.connection.finish()

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

    def on_open(
        self,
        *args,
        **kwargs
    ):

        logger.info(
            "Deepgram websocket opened"
        )

    def on_close(
        self,
        *args,
        **kwargs
    ):

        logger.info(
            "Deepgram websocket closed"
        )

    def on_error(
        self,
        *args,
        **kwargs
    ):

        logger.error(
            f"Deepgram websocket error: "
            f"{args}"
        )

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