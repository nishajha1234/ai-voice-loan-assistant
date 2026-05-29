# app/services/tts_service.py

from deepgram import (
    DeepgramClient,
    SpeakOptions
)

from app.core.config import settings
import uuid
import inspect


class TTSService:

    @staticmethod
    def generate_audio(
    text,
    language="en"
):

        deepgram = DeepgramClient(
            settings.DEEPGRAM_API_KEY
        )

        model = (
            "aura-2-thalia-en"
            if language != "hi"
            else "aura-2-thalia-en"
        )

        options = SpeakOptions(
            model=model
        )

        filename = (
    f"temp_{uuid.uuid4()}.mp3"
)

        speak_client = deepgram.speak.v("1")

        print(inspect.signature(speak_client.save))

        speak_client.save(
            filename,
            {
                "text": text
            },
            options
        )
        return filename