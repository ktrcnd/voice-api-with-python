# VapiVoice Lead API
This project is a Voice-to-Lead Capture API built with FastAPI. It provides backend services that integrate with conversational AI or voice assistants to automatically capture, validate, and enrich lead information in real time.

The API ensures data quality through strict validation rules, enriches records with external information, and stores everything in a structured database. It’s lightweight, zero-cost to run locally, and easy to deploy in production environments.

✨ Features

Lead Management

POST /v1/leads – create new leads with strong validation

GET /v1/leads – list all leads

GET /health – simple status check

Validation Rules

Name must include at least two words

Phone numbers normalized to E.164 format (10–15 digits)

Preferred start time must be at least 48 hours in the future

Reason text constrained to 5–200 characters

Persistence

Uses SQLite + SQLAlchemy ORM for structured storage

Saves both raw and normalized phone numbers

Enrichment

Fetches live USD→EUR exchange rates

Retrieves a short random fun fact (≤80 characters)

Includes retries, 5-second timeouts, and graceful fallback handling

Structured Logging

JSON-formatted logs for each request (method, path, status, latency)

Testing

Comprehensive pytest suite with HTTP mocking

Covers validation errors, persistence, and enrichment success

Zero-Cost Demo

Fully testable locally with curl and ngrok

🛠 Tech Stack

FastAPI – backend web framework

SQLite + SQLAlchemy – lightweight persistence

httpx + tenacity – robust API integrations

phonenumbers – phone number parsing and normalization

pytest + respx – testing and HTTP mocking

ngrok – free tunneling for webhook testing
