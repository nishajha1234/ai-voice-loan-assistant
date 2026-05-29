from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket
from app.db.database import engine
from app.db.models import Base
from app.api.health import router as health_router
from app.api.voice import router as voice_router

from app.websocket.call_ws import websocket_endpoint

from app.core.config import settings

from app.utils.logger import logger
from fastapi.responses import FileResponse
from app.api.dashboard import (
    router as dashboard_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routers
app.include_router(health_router)
app.include_router(voice_router)
app.include_router(
    dashboard_router
)

@app.get("/test")
async def serve_test_page():

    return FileResponse(
        "../frontend/test.html"
    )

@app.get("/")
async def root():

    logger.info(
        "Root endpoint accessed"
    )

    return {
        "message": "AI Voice Loan Assistant Running"
    }


@app.websocket("/ws")
async def websocket_route(
    websocket: WebSocket
):

    logger.info(
        f"Incoming websocket connection "
        f"from {websocket.client}"
    )

    await websocket_endpoint(websocket)