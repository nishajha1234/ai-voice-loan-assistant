# AI Voice Loan Assistant

Realtime AI-powered bilingual loan follow-up assistant built using FastAPI, WebSockets, and streaming audio architecture.

## Current Features

- Realtime browser microphone streaming
- Persistent WebSocket communication
- Audio chunk-based streaming pipeline
- Session lifecycle tracking
- Structured backend logging
- Twilio-ready voice architecture
- Modular FastAPI backend structure

## Current Architecture

```text
Browser Microphone
        ↓
WebSocket Connection
        ↓
FastAPI Backend
        ↓
Realtime Audio Chunk Streaming
        ↓
Future STT / LLM / TTS Pipeline
Tech Stack
FastAPI
WebSockets
Python
Twilio
ngrok
Project Structure
backend/
│
├── app/
│   ├── api/
│   ├── websocket/
│   ├── services/
│   ├── core/
│   └── utils/
│
frontend/
docs/
reports/
recordings/
architecture/
Current Progress
FastAPI backend initialized
WebSocket communication implemented
Browser microphone streaming working
Realtime audio chunks successfully reaching backend
Session tracking and connection logging added
Planned Features
Deepgram realtime speech-to-text
OpenAI realtime conversation engine
Intent detection system
Sentiment analysis
CRM integration
Dashboard analytics
Latency monitoring
Hindi + English bilingual support
Run Locally
Backend
cd backend

venv\Scripts\activate

uvicorn app.main:app --reload
Frontend

Open frontend/test.html using Live Server.