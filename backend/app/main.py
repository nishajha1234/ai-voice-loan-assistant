from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket
from app.api.health import router as health_router
from app.api.voice import router as voice_router
from app.websocket.call_ws import websocket_endpoint

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(voice_router)

@app.get("/")
async def root():
    return {
        "message": "AI Voice Loan Assistant Running"
    }

@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)