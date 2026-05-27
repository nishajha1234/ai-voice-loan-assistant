from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect

from starlette.websockets import (
    WebSocketState
)

from app.services.deepgram_service import (
    DeepgramService
)

from app.utils.logger import logger

import json
import uuid
import time
import asyncio


DEBUG_AUDIO_ACKS = False

MIN_AUDIO_CHUNK_SIZE = 100


async def safe_send_json(
    websocket: WebSocket,
    payload: dict
):

    try:

        if (
            websocket.client_state
            != WebSocketState.CONNECTED
        ):
            return

        await websocket.send_text(
            json.dumps(payload)
        )

    except Exception as e:

        logger.error(
            f"Safe websocket send error: {e}"
        )


async def handle_ping(
    websocket: WebSocket
):

    await safe_send_json(
        websocket,
        {
            "type": "pong"
        }
    )


async def handle_text_message(
    websocket: WebSocket,
    text_data: str,
    session_id: str
):

    logger.info(
        f"[Session {session_id}] "
        f"Text received: {text_data}"
    )

    try:

        parsed = json.loads(text_data)

        if parsed.get("type") == "ping":

            await handle_ping(websocket)

            return

    except Exception:
        pass

    await safe_send_json(
        websocket,
        {
            "type": "text_ack",
            "message": text_data,
            "session_id": session_id
        }
    )


async def handle_audio_chunk(
    websocket: WebSocket,
    audio_chunk: bytes,
    session_id: str,
    chunk_number: int,
    deepgram_service: DeepgramService
):

    chunk_received_at = time.perf_counter()

    chunk_size = len(audio_chunk)

    if chunk_size < MIN_AUDIO_CHUNK_SIZE:
        return

    logger.info(
        f"[Session {session_id}] "
        f"Chunk #{chunk_number} "
        f"({chunk_size} bytes)"
    )

    try:

        deepgram_service.stream_audio(
            audio_chunk
        )

    except Exception as e:

        logger.error(
            f"[Session {session_id}] "
            f"Audio streaming error: {e}"
        )

    if DEBUG_AUDIO_ACKS:

        await safe_send_json(
            websocket,
            {
                "type": "audio_ack",
                "chunk_number": chunk_number,
                "size": chunk_size,
                "received_at": chunk_received_at
            }
        )


async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    session_id = str(uuid.uuid4())

    connection_start_time = time.time()

    audio_chunk_count = 0

    transcript_count = 0

    logger.info(
        f"[Session {session_id}] "
        f"Client connected: "
        f"{websocket.client}"
    )

    deepgram_service = DeepgramService()

    loop = asyncio.get_running_loop()

    async def handle_transcript(
        transcript_data: dict
    ):

        nonlocal transcript_count

        if transcript_data.get("is_final"):
            transcript_count += 1

        transcript_type = (
            "final"
            if transcript_data.get("is_final")
            else "interim"
        )

        await safe_send_json(
            websocket,
            {
                "type": "transcript",
                "transcript_type": transcript_type,
                "data": transcript_data
            }
        )

    def transcript_callback(
        transcript_data: dict
    ):

        future = asyncio.run_coroutine_threadsafe(
            handle_transcript(transcript_data),
            loop
        )

        def callback_done(f):

            exception = f.exception()

            if exception:

                logger.error(
                    f"Transcript callback error: "
                    f"{exception}"
                )

        future.add_done_callback(callback_done)

    deepgram_service.set_transcript_callback(
        transcript_callback
    )

    try:

        await deepgram_service.setup_connection()

        logger.info(
            f"[Session {session_id}] "
            f"Deepgram initialized"
        )

        while True:

            data = await websocket.receive()

            if (
                data["type"]
                == "websocket.disconnect"
            ):

                logger.info(
                    f"[Session {session_id}] "
                    f"Disconnect received"
                )

                break

            if "text" in data:

                text_data = data["text"]

                if text_data is None:
                    continue

                await handle_text_message(
                    websocket,
                    text_data,
                    session_id
                )

            elif "bytes" in data:

                audio_chunk = data["bytes"]

                if audio_chunk is None:
                    continue

                audio_chunk_count += 1

                await handle_audio_chunk(
                    websocket,
                    audio_chunk,
                    session_id,
                    audio_chunk_count,
                    deepgram_service
                )

    except WebSocketDisconnect:

        logger.info(
            f"[Session {session_id}] "
            f"Client disconnected"
        )

    except Exception as e:

        logger.error(
            f"[Session {session_id}] "
            f"WebSocket error: {e}"
        )

    finally:

        duration = round(
            time.time()
            - connection_start_time,
            2
        )

        await deepgram_service.close()

        logger.info(
            f"[Session {session_id}] "
            f"Session duration: "
            f"{duration}s"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Audio chunks: "
            f"{audio_chunk_count}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Final transcripts: "
            f"{transcript_count}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Connection closed"
        )