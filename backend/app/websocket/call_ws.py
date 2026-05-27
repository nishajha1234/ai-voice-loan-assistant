from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.utils.logger import logger

import json
import uuid
import time


async def handle_text_message(
    websocket: WebSocket,
    text_data: str,
    session_id: str
):

    logger.info(
        f"[Session {session_id}] "
        f"Received text: {text_data}"
    )

    if websocket.client_state.name != "CONNECTED":
        return

    await websocket.send_text(
        f"Server received: {text_data}"
    )


async def handle_audio_chunk(
    websocket: WebSocket,
    audio_chunk: bytes,
    session_id: str,
    chunk_number: int
):

    chunk_size = len(audio_chunk)


    # Ignore tiny startup chunks
    if chunk_size < 100:
        return


    logger.info(
        f"[Session {session_id}] "
        f"Chunk #{chunk_number} "
        f"Received audio chunk: "
        f"{chunk_size} bytes"
    )


    if websocket.client_state.name != "CONNECTED":
        return


    await websocket.send_text(
        json.dumps({
            "status": "audio received",
            "size": chunk_size,
            "chunk_number": chunk_number,
            "session_id": session_id
        })
    )


async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()


    session_id = str(uuid.uuid4())

    connection_start_time = time.time()

    audio_chunk_count = 0

    client = websocket.client


    logger.info(
        f"[Session {session_id}] "
        f"Client connected: {client}"
    )


    try:

        while True:

            data = await websocket.receive()

            message_type = data.get("type")


            if message_type == "websocket.disconnect":

                logger.info(
                    f"[Session {session_id}] "
                    f"Disconnect message received"
                )

                break


            if "text" in data:

                await handle_text_message(
                    websocket=websocket,
                    text_data=data["text"],
                    session_id=session_id
                )


            elif "bytes" in data:

                audio_chunk_count += 1

                await handle_audio_chunk(
                    websocket=websocket,
                    audio_chunk=data["bytes"],
                    session_id=session_id,
                    chunk_number=audio_chunk_count
                )


    except WebSocketDisconnect:

        logger.info(
            f"[Session {session_id}] "
            f"Client disconnected cleanly"
        )


    except Exception as e:

        logger.error(
            f"[Session {session_id}] "
            f"WebSocket error: {e}"
        )


    finally:

        duration = round(
            time.time() - connection_start_time,
            2
        )

        logger.info(
            f"[Session {session_id}] "
            f"Session duration: "
            f"{duration} seconds"
        )

        logger.info(
            f"[Session {session_id}] "
            f"Total audio chunks received: "
            f"{audio_chunk_count}"
        )

        logger.info(
            f"[Session {session_id}] "
            f"WebSocket connection closed"
        )