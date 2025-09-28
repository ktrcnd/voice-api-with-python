import os
import tempfile
import json
from fastapi.testclient import TestClient
import respx
import httpx
import pytest

from app.main import app
from app.db import SessionLocal, engine
from app.models import Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_valid_post_creates_record(monkeypatch):
    payload = {
        "name": "John Doe",
        "phone": "+14155552671",
        "preferred_start": "2025-09-28T14:00:00Z",
        "preferred_end": "2025-09-28T15:00:00Z",
        "reason": "Severe headache",
        "utc_offset": "-05:00",
        "call_id": "test-call-123"
    }
    response = client.post("/v1/leads", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["id"], int)

def test_invalid_phone_rejected():
    payload = {
        "name": "John Doe",
        "phone": "1234",
        "preferred_start": "2025-09-28T15:00:00Z",
        "reason": "Severe headache"
    }
    response = client.post("/v1/leads", json=payload)
    assert response.status_code == 422 or response.status_code == 400

def test_enrichment_mocked(respx_mock):
    # mock fx and catfact endpoisnt
    fx_route = respx_mock.get("https://api.exchangerate.host/latest").respond(
        json={
            "success": True,
            "timestamp": "1664198400",
            "base": "USD",
            "date": "2025-09-27",
            "rates": {
                "EUR": 0.03
            } 
        }
    )
    fact_route = respx_mock.get("https://catfact.ninja/fact").respond(
        json={"fact": "Cats are great animals that purr and nap all day long."}, status_code=200
    )

    payload = {
        "name": "Neil Smith",
        "phone": "+15555550123",
        "preferred_start": "2030-09-29T16:00:00Z",
        "reason": "Consultation"
    }
    resp = client.post("/v1/leads", json=payload)
    assert resp.status_code == 200
    id_ = resp.json()["id"]

    # retrieve leasd
    list_resp = client.get("/v1/leads")
    assert list_resp.status_code == 200
    leads = list_resp.json()

    #find lead by uisgn id
    lead = next((l for l in leads if l["id"] == id_), None)
    assert lead is not None
    assert lead["fx_usd_eur"] == 0.03
    assert lead["fun_fact_shorts"].startswith("Cats are great")