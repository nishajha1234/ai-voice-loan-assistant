# AI Voice Calling Assistant for Loan Follow-Up & Customer Support

## Overview

AI Voice Calling Assistant is a real-time voice-based loan support system built using FastAPI, WebSockets, Deepgram Speech-to-Text, Deepgram Text-to-Speech, and SQLite.

The system enables automated loan follow-up conversations, customer query handling, intent detection, sentiment analysis, callback scheduling, hot-lead identification, CRM persistence, and real-time dashboard analytics.

This project was developed as part of a technical evaluation focused on real-time voice AI systems.

---

## Features

### Real-Time Voice Pipeline

* Live audio streaming using WebSockets
* Deepgram Realtime Speech-to-Text
* Deepgram Text-to-Speech
* Low-latency conversational flow
* Real-time transcript updates

### Intent Detection

The assistant detects customer intent during live conversations:

* Interested
* Confused
* Angry
* Spam / Invalid
* High-Ticket Lead
* Callback Request
* EMI Query
* Document Query
* Escalation Request
* Call End

### Conversation Management

Supported conversation flows:

* Greeting Flow
* Loan Eligibility Discussion
* EMI Queries
* Document Requirements
* Objection Handling
* Callback Booking
* Human Escalation
* Call Termination

### CRM Integration

After every session, the system stores:

* Session ID
* Transcript
* Intent
* Sentiment
* Conversation State
* AI Response
* Call Duration
* Language

### Notifications

Hot leads automatically trigger Slack notifications for:

* Interested Customers
* High-Ticket Leads

### Dashboard Analytics

Dashboard provides:

* Total Calls
* Conversion Rate
* Intent Analytics
* Sentiment Analytics
* Recent Calls
* Transcript History
* Hot Leads
* Audio Playback
* Recording Management

### Call Recording

The system stores:

* Customer Audio
* AI Audio Responses

Recordings are accessible directly from the dashboard.

---

## Technology Stack

### Backend

* FastAPI
* Python
* WebSockets

### Voice AI

* Deepgram Realtime STT
* Deepgram TTS

### Database

* SQLite
* SQLAlchemy ORM

### Frontend

* HTML
* CSS
* JavaScript

### Integrations

* Slack Webhooks

---

## System Architecture

```text
Customer Browser
        │
        ▼
FastAPI WebSocket Server
        │
        ▼
Deepgram Realtime STT
        │
        ▼
Intent Detection
State Management
Sentiment Analysis
        │
        ▼
Response Service
        │
        ▼
Deepgram TTS
        │
        ▼
Audio Playback

        │
        ▼

CRM Service
        │
        ▼
SQLite Database

        │
        ▼

Dashboard Analytics
```

---

## Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── services/
│   ├── utils/
│   └── websocket/
│
├── recordings/
│
├── frontend/
│
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ai-voice-loan-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
DEEPGRAM_API_KEY=your_deepgram_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
SLACK_WEBHOOK_URL=your_webhook_url
```

### Run Application

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Dashboard Summary

```http
GET /dashboard/summary
```

### Dashboard Sentiment Analytics

```http
GET /dashboard/sentiment
```

### Dashboard Hot Leads

```http
GET /dashboard/hot-leads
```

### Dashboard Recordings

```http
GET /dashboard/recordings
```

### WebSocket Audio Streaming

```http
WS /ws
```

---

## Dashboard Metrics

The dashboard tracks:

* Total Calls
* Interested Leads
* Callback Requests
* High-Ticket Leads
* Angry Customers
* Conversion Rate
* Sentiment Distribution
* Intent Accuracy
* False Positive Rate

---

## Scalability Roadmap

To support a larger number of concurrent calls:

- Deploy multiple FastAPI instances behind a load balancer.
- Replace SQLite with a production database.
- Move notification and reporting tasks to background workers.
- Store recordings in cloud storage.
- Add monitoring and logging for system health.

---

## Current Limitations

* Rule-based response generation
* Manual language selection during testing
* SQLite used for simplicity
* Twilio outbound calling not fully tested in production environment

---

## Future Improvements

* Improve conversation quality using an LLM-based response engine.
* Add automatic language detection for Hindi and English conversations.
* Improve speech recognition accuracy for noisy environments.
* Enhance intent detection with machine learning models.
* Add production-ready Twilio calling support.
* Improve dashboard analytics and reporting.

---

## Author

Nisha Jha
