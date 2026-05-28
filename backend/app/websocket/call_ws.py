from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect

from starlette.websockets import (
    WebSocketState
)

from app.services.deepgram_service import (
    DeepgramService
)

from app.services.session_manager import (
    SessionManager
)

from app.services.intent_service import (
    IntentService
)

from app.services.state_service import (
    StateService
)

from app.core.constants import (
    MIN_AUDIO_CHUNK_SIZE,
    AUDIO_LOG_INTERVAL,
    DEBUG_AUDIO_ACKS
)

from app.utils.logger import logger

import json
import uuid
import time
import asyncio


# ============================================
# SAFE JSON SENDER
# ============================================

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


# ============================================
# PING HANDLER
# ============================================

async def handle_ping(
    websocket: WebSocket
):

    await safe_send_json(
        websocket,
        {
            "type": "pong"
        }
    )


# ============================================
# TEXT MESSAGE HANDLER
# ============================================

async def handle_text_message(
    websocket: WebSocket,
    text_data: str,
    session_id: str,
    session_manager: SessionManager,
    deepgram_service: DeepgramService
):

    logger.info(
        f"[Session {session_id}] "
        f"Text received: {text_data}"
    )

    try:

        parsed = json.loads(text_data)

        # -----------------------------------
        # KEEPALIVE PING
        # -----------------------------------

        if parsed.get("type") == "ping":

            await handle_ping(websocket)

            return

        # -----------------------------------
        # LANGUAGE CONFIGURATION
        # -----------------------------------

        if parsed.get("type") == "language_config":

            selected_language = (
                parsed.get("language", "multi")
            )

            session_manager.language = (
                selected_language
            )

            logger.info(
                f"[Session {session_id}] "
                f"Language set to: "
                f"{selected_language}"
            )

            # -----------------------------------
            # INITIALIZE DEEPGRAM
            # -----------------------------------

            if not deepgram_service.connection:

                await deepgram_service.setup_connection(
                    language=selected_language
                )

                logger.info(
                    f"[Session {session_id}] "
                    f"Deepgram initialized "
                    f"with language: "
                    f"{selected_language}"
                )

            await safe_send_json(
                websocket,
                {
                    "type": "language_updated",
                    "language": selected_language
                }
            )

            return

    except Exception as e:

        logger.error(
            f"[Session {session_id}] "
            f"Text parse error: {e}"
        )

    await safe_send_json(
        websocket,
        {
            "type": "text_ack",
            "message": text_data,
            "session_id": session_id
        }
    )


# ============================================
# AUDIO CHUNK HANDLER
# ============================================

async def handle_audio_chunk(
    websocket: WebSocket,
    audio_chunk: bytes,
    session_id: str,
    chunk_number: int,
    deepgram_service: DeepgramService
):

    chunk_size = len(audio_chunk)

    if chunk_size < MIN_AUDIO_CHUNK_SIZE:
        return

    # -----------------------------------
    # REDUCE EXCESSIVE LOGGING
    # -----------------------------------

    if chunk_number % AUDIO_LOG_INTERVAL == 0:

        logger.info(
            f"[Session {session_id}] "
            f"Chunk #{chunk_number} "
            f"({chunk_size} bytes)"
        )

    # -----------------------------------
    # STREAM AUDIO TO DEEPGRAM
    # -----------------------------------

    try:

        if deepgram_service.connection:

            deepgram_service.stream_audio(
                audio_chunk
            )

    except Exception as e:

        logger.error(
            f"[Session {session_id}] "
            f"Audio streaming error: {e}"
        )

    # -----------------------------------
    # OPTIONAL DEBUG ACKS
    # -----------------------------------

    if DEBUG_AUDIO_ACKS:

        await safe_send_json(
            websocket,
            {
                "type": "audio_ack",
                "chunk_number": chunk_number,
                "size": chunk_size
            }
        )


# ============================================
# MAIN WEBSOCKET ENDPOINT
# ============================================

async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    # ========================================
    # SESSION SETUP
    # ========================================

    session_id = str(uuid.uuid4())

    connection_start_time = time.time()

    audio_chunk_count = 0

    transcript_count = 0

    session_manager = SessionManager()

    logger.info(
        f"[Session {session_id}] "
        f"Client connected: "
        f"{websocket.client}"
    )

    # ========================================
    # SEND SESSION START EVENT
    # ========================================

    await safe_send_json(
        websocket,
        {
            "type": "session_started",
            "session_id": session_id,
            "started_at": connection_start_time
        }
    )

    # ========================================
    # DEEPGRAM SERVICE
    # ========================================

    deepgram_service = DeepgramService()

    loop = asyncio.get_running_loop()

    # ========================================
    # TRANSCRIPT HANDLER
    # ========================================

    async def handle_transcript(
        transcript_data: dict
    ):

        nonlocal transcript_count

        is_final = (
            transcript_data.get("is_final")
        )

        transcript_data[
            "transcript_processed_at"
        ] = time.perf_counter()

        # ====================================
        # FINAL TRANSCRIPT LOGIC
        # ====================================

        if is_final:

            transcript_count += 1

            session_manager.increment_final_transcripts()

            transcript = (
                transcript_data["transcript"]
            )

            # --------------------------------
            # STORE HISTORY
            # --------------------------------

            session_manager.add_transcript(
                transcript
            )

            # --------------------------------
            # INTENT DETECTION
            # --------------------------------

            intent = (
                IntentService.detect_intent(
                    transcript
                )
            )

            session_manager.update_intent(
                intent
            )

            # --------------------------------
            # STATE TRANSITIONS
            # --------------------------------

            next_state = (
                StateService.determine_next_state(
                    session_manager.current_state,
                    intent,
                    transcript
                )
            )

            session_manager.update_state(
                next_state
            )

            transcript_data["intent"] = (
                intent
            )

            transcript_data["state"] = (
                next_state
            )

            logger.info(
                f"[Session {session_id}] "
                f"Intent detected: "
                f"{intent}"
            )

            logger.info(
                f"[Session {session_id}] "
                f"Next state: "
                f"{next_state}"
            )

        # ====================================
        # DEFAULT FALLBACKS
        # ====================================

        if "intent" not in transcript_data:

            transcript_data["intent"] = (
                session_manager.current_intent
            )

        if "state" not in transcript_data:

            transcript_data["state"] = (
                session_manager.current_state
            )

        transcript_type = (
            "final"
            if is_final
            else "interim"
        )

        # ====================================
        # SEND TO FRONTEND
        # ====================================

        await safe_send_json(
            websocket,
            {
                "type": "transcript",
                "transcript_type": transcript_type,
                "data": transcript_data
            }
        )

    # ========================================
    # THREADSAFE CALLBACK BRIDGE
    # ========================================

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

    # ========================================
    # MAIN RECEIVE LOOP
    # ========================================

    try:

        while True:

            data = await websocket.receive()

            # -----------------------------------
            # DISCONNECT EVENT
            # -----------------------------------

            if (
                data["type"]
                == "websocket.disconnect"
            ):

                logger.info(
                    f"[Session {session_id}] "
                    f"Disconnect received"
                )

                break

            # -----------------------------------
            # TEXT EVENTS
            # -----------------------------------

            if "text" in data:

                text_data = data["text"]

                if text_data is None:
                    continue

                await handle_text_message(
                    websocket,
                    text_data,
                    session_id,
                    session_manager,
                    deepgram_service
                )

            # -----------------------------------
            # AUDIO EVENTS
            # -----------------------------------

            elif "bytes" in data:

                audio_chunk = data["bytes"]

                if audio_chunk is None:
                    continue

                audio_chunk_count += 1

                session_manager.increment_audio_chunks()

                await handle_audio_chunk(
                    websocket,
                    audio_chunk,
                    session_id,
                    audio_chunk_count,
                    deepgram_service
                )

    # ========================================
    # DISCONNECT HANDLING
    # ========================================

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

    # ========================================
    # CLEANUP
    # ========================================

    finally:

        duration = round(
            time.time()
            - connection_start_time,
            2
        )

        # ====================================
        # SAFE WEBSOCKET CLOSE
        # ====================================

        if (
            websocket.client_state
            == WebSocketState.CONNECTED
        ):

            await websocket.close()

            logger.info(
                f"[Session {session_id}] "
                f"WebSocket connection closed safely"
            )

        # ====================================
        # CLOSE DEEPGRAM
        # ====================================

        await deepgram_service.close()

        logger.info(
            f"[Session {session_id}] "
            f"Session duration: "
            f"{duration}s"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Audio chunks: "
            f"{session_manager.total_audio_chunks}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Final transcripts: "
            f"{session_manager.total_final_transcripts}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Current intent: "
            f"{session_manager.current_intent}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Final state: "
            f"{session_manager.current_state}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Connection closed"
        )