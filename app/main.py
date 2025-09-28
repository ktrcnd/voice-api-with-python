import time
import logging

from logging import StreamHandler
from pythonjsonlogger import jsonlogger

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.orm import Session

from .db import SessionLocal, engine
from .models import Base, Lead
from .schemas import LeadCreate, LeadOut
from .services import enrichment, utils

Base.metadata.create_all(bind=engine)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = StreamHandler()
formatter = jsonlogger.JsonFormatter('%(acstime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title="Vapi Voice + Python API (WiseWork Tech Test)")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def add_logging(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as exc:
        status_code = 500
        raise
    finally:
        latency = round((time.time() - start) * 1000, 2)
        logger.info("route=%s method=%s path=%s status=%s latency=%s",
                    request.method, request.method, request.url.path, status_code, latency)
        
    return response

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/leads")
def create_lead(payload: LeadCreate, requests: Request):
    #validate and create Lead
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    db: Session = next(get_db())

    # Normalize Phone
    normalized = utils.normalized_phone(payload.phone)

    lead = Lead(
        name = payload.name,
        phone = payload.phone,
        normalized_phone = normalized,
        preferred_start = payload.preferred_start,
        preferred_end = payload.preferred_end,
        reason = payload.reason
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    #Enrichment --> attempts; failures Logged but do not fail request
    try:
        fx = enrichment.fetch_fx_usd_eur()
        if fx is not None:
            lead.fx_usd_eur = fx
    except Exception as e:
        logger.error("fx enrichment failed: %s", str(e))
    
    try:
        fact = enrichment.fetch_fun_fact_short(80)
        if fact:
            lead.fun_fact_short = fact
    except Exception as e:
        logger.error("funfact enrichment failed: %s", str(e))

    try:
        db.add(lead)
        db.commit()
    except Exception as e:
        logger.error("db update failed: %s", str(e))

    logger.info("lead_created id=%s name=%s call_id=%s", lead.id, lead.name, payload.call_id)
    return JSONResponse(status_code=200, content = jsonable_encoder({"status": "ok", "id": lead.id}))

@app.get("/v1/leads", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.id.desc()).all()
    return [LeadOut.from_orm(l) for l in leads]