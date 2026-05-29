# Estimated Latency Analysis

## Project

AI Voice Calling Assistant for Loan Follow-Up & Customer Support

---

## Overview

This document provides an estimated latency analysis of the voice assistant pipeline based on observed system behavior during testing.

The current implementation uses:

* FastAPI
* WebSockets
* Deepgram Realtime Speech-to-Text
* Intent Detection Engine
* Conversation State Management
* Deepgram Text-to-Speech
* SQLite CRM Storage
* Analytics Dashboard

At the current project stage, detailed component-level telemetry and distributed tracing have not been implemented. Therefore, the values below represent estimated latency ranges derived from testing observations and expected service performance.

---

## Voice Processing Pipeline

```text
Customer Audio
      │
      ▼
Browser Audio Capture
      │
      ▼
WebSocket Streaming
      │
      ▼
Deepgram Realtime STT
      │
      ▼
Intent Detection
      │
      ▼
State Management
      │
      ▼
Response Generation
      │
      ▼
Deepgram TTS
      │
      ▼
Browser Audio Playback
```

---

## Estimated Latency Breakdown

| Component             | Estimated Latency |
| --------------------- | ----------------- |
| Audio Capture         | 50–150 ms         |
| WebSocket Transfer    | 50–100 ms         |
| Deepgram Realtime STT | 300–700 ms        |
| Intent Detection      | <10 ms            |
| State Management      | <5 ms             |
| Response Generation   | 10–30 ms          |
| Deepgram TTS          | 500–1000 ms       |
| Audio Playback        | 100–200 ms        |

---

## Estimated End-to-End Latency

Minimum Estimated Latency:

```text
50 + 50 + 300 + 10 + 5 + 10 + 500 + 100
≈ 1.0 second
```

Typical Estimated Latency:

```text
100 + 80 + 450 + 10 + 5 + 20 + 700 + 150
≈ 1.5 seconds
```

Worst Case Estimated Latency:

```text
150 + 100 + 700 + 10 + 5 + 30 + 1000 + 200
≈ 2.2 seconds
```

---

## Assignment Requirement Validation

Assignment Requirement:

```text
Response latency must remain under 2.5 seconds.
```

Based on testing observations and estimated component performance, the implemented architecture is expected to remain within the required latency threshold under normal operating conditions.

Estimated Typical Latency:

```text
≈ 1.5 seconds
```

Estimated Worst Case Latency:

```text
≈ 2.2 seconds
```

Both values remain below the required 2.5-second limit.

---

## Current Limitation

The current version does not include:

* Per-component latency instrumentation
* Distributed tracing
* End-to-end latency monitoring dashboards
* Automated performance benchmarking

Latency values in this document are estimates and should not be considered production-grade benchmark measurements.

---

## Future Improvements

For production deployment, latency measurement can be improved through:

* Request tracing
* OpenTelemetry integration
* Prometheus metrics collection
* Grafana dashboards
* Deepgram API timing metrics
* WebSocket performance monitoring
* End-to-end response tracking

---

## Conclusion

The implemented voice assistant architecture supports real-time conversational interactions through streaming speech recognition, intent detection, state management, speech synthesis, CRM integration, and analytics reporting.

Based on observed testing behavior, the system is expected to operate within the assignment requirement of maintaining response latency below 2.5 seconds.
