# 🎙️ VapiVoice Lead API

A **Voice-to-Lead Capture API** built with [FastAPI](https://fastapi.tiangolo.com/).  
It integrates with conversational AI or voice assistants to **capture, validate, and enrich lead information in real time**.

The API ensures high-quality data through strict validation rules, external enrichment, and structured persistence — all while being **lightweight, free to run locally, and production-ready**.

---

## ✨ Features

### 📌 Lead Management
- `POST /v1/leads` – Create new leads with strict validation  
- `GET /v1/leads` – List all stored leads  
- `GET /health` – Simple status check  

### 🔒 Validation Rules
- Name must include **at least two words**  
- Phone numbers normalized to **E.164 format** (10–15 digits)  
- Preferred start time must be **≥48 hours in the future**  
- Reason text must be **5–200 characters**  

### 💾 Persistence
- **SQLite + SQLAlchemy ORM** for structured storage  
- Stores both **raw and normalized phone numbers**  

### 🌍 Enrichment
- Fetches live **USD → EUR exchange rates**  
- Retrieves a short random **fun fact (≤80 characters)**  
- Includes **retries, 5s timeouts, and graceful fallback handling**  

### 📑 Structured Logging
- **JSON-formatted logs** per request  
- Includes method, path, status, and latency  

### 🧪 Testing
- Comprehensive **pytest** suite with HTTP mocking  
- Covers validation errors, persistence, and enrichment success  

### 🚀 Zero-Cost Demo
- Fully testable **locally** with `curl` and [ngrok](https://ngrok.com/)  

---

## 🛠 Tech Stack
- **FastAPI** – Modern Python web framework  
- **SQLite + SQLAlchemy** – Lightweight database + ORM  
- **httpx + tenacity** – Robust API integrations  
- **phonenumbers** – Parsing & normalizing phone numbers  
- **pytest + respx** – Testing & HTTP mocking  
- **ngrok** – Free tunneling for webhook testing  

---

## ⚡ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/vapivoice-lead-api.git
cd vapivoice-lead-api

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