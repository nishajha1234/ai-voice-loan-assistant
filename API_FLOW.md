# API Flow Explanation

## Overview

The AI Voice Loan Assistant is built using FastAPI, WebSockets, Deepgram STT/TTS, SQLite, and a real-time dashboard.

The system processes customer speech in real time, detects intent, generates responses, stores conversation data, and updates analytics.

---

## Flow

### 1. User Starts Conversation

* User opens the dashboard.
* Browser establishes a WebSocket connection with FastAPI.
* A unique session ID is created.

### 2. Audio Streaming

* User speech is captured through the microphone.
* Audio chunks are streamed to FastAPI via WebSocket.
* FastAPI forwards audio to Deepgram Realtime STT.

### 3. Speech-to-Text

* Deepgram converts speech into text.
* Interim and final transcripts are generated.

### 4. Intent Detection

The system analyzes final transcripts and detects intents such as:

* Interested
* Callback
* EMI Query
* Document Query
* Angry
* High Ticket
* Escalation Request

### 5. State Management

Based on the detected intent, the conversation moves to the appropriate state:

* Eligibility
* EMI Discussion
* Document Reminder
* Callback Booking
* Escalation
* Call End

### 6. Response Generation

The Response Service generates a contextual reply based on:

* Intent
* Conversation State
* Selected Language

### 7. Text-to-Speech

* Response text is sent to Deepgram TTS.
* Audio is generated and returned to the browser.
* The customer hears the AI response.

### 8. CRM Storage

The system stores:

* Transcript
* Intent
* Sentiment
* Conversation State
* Session Duration
* Language

in the SQLite database.

### 9. Notifications

For hot leads such as:

* Interested
* Callback
* High Ticket

the system sends Slack alerts automatically.

### 10. Dashboard Analytics

The dashboard displays:

* Total Calls
* Live Transcripts
* Intent Analytics
* Sentiment Metrics
* Hot Leads
* Conversion Rate
* Call Recordings

---

## End-to-End Pipeline

Customer Speech

↓

WebSocket

↓

FastAPI

↓

Deepgram STT

↓

Intent Detection

↓

State Management

↓

Response Generation

↓

Deepgram TTS

↓

Audio Playback

↓

CRM Storage & Dashboard Analytics
