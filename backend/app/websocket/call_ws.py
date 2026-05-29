from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect

from starlette.websockets import (
    WebSocketState
)

from app.services.crm_service import (
    CRMService
)

from app.services.response_service import (
    ResponseService
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

from app.services.sentiment_service import (
    SentimentService
)
from app.services.tts_service import (
    TTSService
)

import uuid
import time
import asyncio
import json
import base64
import os


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

        await websocket.send_json(payload)

    except RuntimeError:

        logger.warning(
            "WebSocket already closed"
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

        # ====================================
        # KEEPALIVE PING
        # ====================================

        if parsed.get("type") == "ping":

            await handle_ping(websocket)

            return

        # ====================================
        # LANGUAGE CONFIG
        # ====================================

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

            # ====================================
            # INITIALIZE DEEPGRAM
            # ====================================

            if not deepgram_service.connection_ready:

                logger.info(
                    f"[Session {session_id}] "
                    f"Initializing Deepgram..."
                )

                connection_success = (
                    await deepgram_service.setup_connection(
                        language=selected_language
                    )
                )

                if not connection_success:

                    logger.error(
                        f"[Session {session_id}] "
                        f"Deepgram initialization failed"
                    )

                    await safe_send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": (
                                "Failed to connect "
                                "to Deepgram"
                            )
                        }
                    )

                    return

                logger.info(
                    f"[Session {session_id}] "
                    f"Deepgram initialized"
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

    # ========================================
    # REDUCE EXCESSIVE LOGGING
    # ========================================

    if chunk_number % AUDIO_LOG_INTERVAL == 0:

        logger.info(
            f"[Session {session_id}] "
            f"Chunk #{chunk_number} "
            f"({chunk_size} bytes)"
        )

    # ========================================
    # STREAM AUDIO
    # ========================================

    try:

        if (
            deepgram_service.connection_ready
            and deepgram_service.connection
        ):

            deepgram_service.stream_audio(
                audio_chunk
            )

    except Exception as e:

        logger.error(
            f"[Session {session_id}] "
            f"Audio streaming error: {e}"
        )

    # ========================================
    # OPTIONAL DEBUG ACKS
    # ========================================

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
    # SESSION START EVENT
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

        if not session_manager.is_active:

            logger.warning(
                f"[Session {session_id}] "
                f"Ignoring transcript after session closed"
            )

            return

        try:

            transcript = (
                transcript_data.get(
                    "transcript",
                    ""
                ).strip()
            )

            if not transcript:
                return

            is_final = (
                transcript_data.get(
                    "is_final",
                    False
                )
            )

            transcript_type = (
                "final"
                if is_final
                else "interim"
            )

            transcript_data[
                "transcript_processed_at"
            ] = time.perf_counter()

            current_intent = (
                session_manager.current_intent
            )

            current_state = (
                session_manager.current_state
            )

            ai_response = ""
            
            sentiment = "NEUTRAL"
            
            audio_bytes = None

            # ====================================
            # FINAL TRANSCRIPT FLOW
            # ====================================

            if is_final:

                transcript_count += 1

                session_manager.increment_final_transcripts()

                session_manager.add_transcript(
                    transcript
                )
                
                sentiment = (
    SentimentService.detect_sentiment(
        transcript
    )
)

                current_intent = (
                    IntentService.detect_intent(
                        transcript
                    )
                )

                session_manager.update_intent(
                    current_intent
                )

                current_state = (
                    StateService.determine_next_state(
                        session_manager.current_state,
                        current_intent,
                        transcript
                    )
                )

                session_manager.update_state(
                    current_state
                )

                ai_response = (
    ResponseService.generate_response(
        intent=current_intent,
        state=current_state,
        language=session_manager.language,
        transcript=transcript
    )
)
                
                audio_file = (
    TTSService.generate_audio(
        text=ai_response,
        language=session_manager.language
    )
)
                with open(
                audio_file,
                "rb"
            ) as file:

                    audio_bytes = (
                        base64.b64encode(
                            file.read()
                        ).decode()
                    )
                    
            try:
                os.remove(audio_file)

            except Exception:
                pass                    

                logger.info(
                    f"[Session {session_id}] "
                    f"Intent detected: "
                    f"{current_intent}"
                )

                logger.info(
                    f"[Session {session_id}] "
                    f"Next state: "
                    f"{current_state}"
                )

                logger.info(
                    f"[Session {session_id}] "
                    f"AI response: "
                    f"{ai_response}"
                )

                # ====================================
                # SAVE TO CRM
                # ====================================

                try:

                    await asyncio.to_thread(
                        CRMService.save_transcript,
                        session_id=session_id,
                        transcript=transcript,
                        transcript_type=transcript_type,
                        intent=str(current_intent),
                        state=str(current_state),
                        sentiment=sentiment,
                        ai_response=ai_response
                    )

                except Exception as db_error:

                    logger.error(
                        f"CRM save error: {db_error}"
                    )

            # ====================================
            # RESPONSE PAYLOAD
            # ====================================

            transcript_data["intent"] = (
                current_intent
            )

            transcript_data["state"] = (
                current_state
            )
            
            transcript_data["sentiment"] = (
    sentiment
)


            transcript_data["ai_response"] = (
                ai_response
            )

            # ====================================
            # SEND TO FRONTEND
            # ====================================

            await safe_send_json(
                websocket,
                {
                    "type": "transcript",
                    "transcript_type": transcript_type,
                    "data": transcript_data,
                    "audio": audio_bytes,
                }
            )

        except Exception as e:

            logger.error(
                f"handle_transcript error: {e}"
            )

    # ========================================
    # THREADSAFE CALLBACK BRIDGE
    # ========================================

    def transcript_callback(
        transcript_data: dict
    ):

        try:

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

            future.add_done_callback(
                callback_done
            )

        except Exception as e:

            logger.error(
                f"run_coroutine_threadsafe failed: {e}"
            )

    deepgram_service.set_transcript_callback(
        transcript_callback
    )

    # ========================================
    # MAIN RECEIVE LOOP
    # ========================================

    try:

        while True:

            message = await websocket.receive()

            # ====================================
            # DISCONNECT
            # ====================================

            if (
                message["type"]
                == "websocket.disconnect"
            ):

                logger.info(
                    f"[Session {session_id}] "
                    f"Disconnect received"
                )

                break

            # ====================================
            # TEXT EVENTS
            # ====================================

            text_data = message.get("text")

            if text_data is not None:

                await handle_text_message(
                    websocket,
                    text_data,
                    session_id,
                    session_manager,
                    deepgram_service
                )

                continue

            # ====================================
            # AUDIO EVENTS
            # ====================================

            audio_chunk = message.get("bytes")

            if audio_chunk is not None:

                audio_chunk_count += 1

                session_manager.increment_audio_chunks()

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

        logger.exception(
            f"[Session {session_id}] "
            f"WebSocket fatal error: {e}"
        )

    # ========================================
    # CLEANUP
    # ========================================

    finally:
        
        session_manager.is_active = False

        logger.info(
            f"[Session {session_id}] "
            f"Session marked inactive"
        )

        duration = round(
            time.time()
            - connection_start_time,
            2
        )

        # ====================================
        # SAVE SESSION SUMMARY
        # ====================================

        try:

            await asyncio.to_thread(
                CRMService.save_session_summary,
                session_id,
                session_manager,
                duration
            )

        except Exception as summary_error:

            logger.error(
                f"Session summary save error: "
                f"{summary_error}"
            )

        # ====================================
        # SAFE SOCKET CLOSE
        # ====================================

        try:

            if (
                websocket.client_state
                == WebSocketState.CONNECTED
            ):

                await websocket.close()

        except Exception as close_error:

            logger.error(
                f"WebSocket close error: "
                f"{close_error}"
            )

        # ====================================
        # CLOSE DEEPGRAM
        # ====================================

        await deepgram_service.close()

        # ====================================
        # FINAL METRICS
        # ====================================

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