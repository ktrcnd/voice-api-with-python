# 🎙️ VapiVoice Lead API

A **Voice-to-Lead Capture API** built with [FastAPI](https://fastapi.tiangolo.com/).  
It connects with conversational AI platforms like **Vapi.ai** to automatically **collect, validate, and store lead information** in real time.

This API validates user inputs, enriches the data (e.g. currency rates and fun facts), and stores it locally in a lightweight SQLite database — perfect for local testing and Vapi.ai integration.

---

## ✨ Features

### 📌 Lead Management
- `POST /v1/leads` – Create new leads with strict validation  
- `GET /v1/leads` – List all stored leads  
- `GET /health` – Simple status check  

### 🔒 Validation Rules
- Full name must include **at least two words**  
- Phone number must be in **E.164 format** (10–15 digits)  
- Preferred start time must be **at least 48 hours in the future**  
- Reason field must be **5–200 characters**

### 💾 Data Storage
- Uses **SQLite + SQLAlchemy ORM**  
- Automatically creates `leads.db` (no setup required)  
- Stores raw and normalized data for accuracy

### 🌍 Data Enrichment
- Fetches **USD → EUR exchange rate**  
- Adds a random **fun fact (≤80 characters)**  
- Includes retry logic and timeout handling

### 🧾 Structured Logging
- JSON-formatted logs per request  
- Includes request method, path, status, and latency

### 🧪 Testing
- Fully tested with **pytest** + **respx**  
- Includes validation, enrichment, and persistence checks

### 🚀 Zero-Cost Setup
- 100% free to run locally  
- Works with **ngrok** for public webhook testing  

---

## 🛠 Tech Stack

| Component | Description |
|------------|-------------|
| **FastAPI** | Modern, high-performance web framework |
| **SQLite + SQLAlchemy** | Lightweight database and ORM |
| **httpx + tenacity** | Reliable async HTTP calls with retries |
| **phonenumbers** | For parsing and validating phone numbers |
| **pytest + respx** | Testing and HTTP mocking |
| **ngrok** | Free tunneling for webhook testing |

---

## ⚡ Getting Started (Quick Setup Guide)

This guide is designed for **non-technical users** to easily set up and run the API locally.

---

### 🧩 Prerequisites

Before you start, install the following:
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [ngrok](https://ngrok.com/download)

---

## ⚡ Getting Started

### 1. Clone the repo
```bash
git clone the project
cd voice-api-with-python in the terminal

## Setup (local, zero-cost)
#### 1. Create venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate

### 2. Install requirements.txt
    pip install -r requirements.txt

### 3. Create .env from .env.example if desired (default uses sqlite ./leads.db).

### 4. Run Server:
    uvicorn app.main:app --port 8000

### 5. Expose with ngrok (This is free plan only):
    ngrok http 8000
    #### You’ll get a forwarding link like: Forwarding  https://abcd1234.ngrok-free.app -> http://localhost:8000
    ### Copy the HTTPS URL (for example:
        👉 https://abcd1234.ngrok-free.app)

### 6. Connect to Vapi.ai
    ### In your Vapi Assistant settings, go to Webhook Target and paste:
    https://abcd1234.ngrok-free.app/v1/leads

### 7. You can test manually using curl or Postman.
    curl -X POST http://127.0.0.1:8000/v1/leads \
        -H "Content-Type: application/json" \
        -d '{
        "name": "Jane Doe",
        "phone": "+14155552671",
        "preferred_start": "2025-10-10T10:00:00Z",
        "reason": "Dental checkup"
    }'
    
    Response:
        {
            "id": 1,
            "name": "Jane Doe",
            "phone": "+14155552671",
            "preferred_start": "2025-10-10T10:00:00Z",
            "reason": "Dental checkup",
            "usd_to_eur": 0.92,
            "fun_fact": "Honey never spoils."
        }
