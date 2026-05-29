from pathlib import Path
import wave


class RecordingService:

    RECORDINGS_DIR = Path("recordings")

    @classmethod
    def initialize(cls):
        cls.RECORDINGS_DIR.mkdir(
            exist_ok=True
        )

    @classmethod
    def save_chunk(
        cls,
        session_id: str,
        audio_chunk: bytes
    ):
        pcm_file = (
            cls.RECORDINGS_DIR /
            f"{session_id}.pcm"
        )

        with open(
            pcm_file,
            "ab"
        ) as file:
            file.write(audio_chunk)

    @classmethod
    def finalize(
        cls,
        session_id: str
    ):
        pcm_file = (
            cls.RECORDINGS_DIR /
            f"{session_id}.pcm"
        )

        wav_file = (
            cls.RECORDINGS_DIR /
            f"{session_id}.wav"
        )

        if not pcm_file.exists():
            return

        with open(
            pcm_file,
            "rb"
        ) as pcm:

            pcm_data = pcm.read()

        with wave.open(
            str(wav_file),
            "wb"
        ) as wav:

            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)

            wav.writeframes(
                pcm_data
            )