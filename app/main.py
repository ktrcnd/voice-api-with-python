import time
import logging
from logging import StreamHandler
from fastapi.middleware.cors import CORSMiddleware
from pythonjsonlogger import jsonlogger

from fastapi import Request, FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from .db import SessionLocal, engine
from .models import Base, Lead
from .schemas import LeadCreate, LeadOut, LeadWrapper
from .services import enrichment, utils

# Create tables
Base.metadata.create_all(bind=engine)

# Logging setup
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# FastAPI app
app = FastAPI(title="Vapi Voice + Python API (WiseWork Tech Test)")

# CORS middleware (allow all origins for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware for logging requests
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
        logger.info(
            "route=%s method=%s path=%s status=%s latency=%s",
            request.url.path,
            request.method,
            request.url.path,
            status_code,
            latency,
        )
    return response

# Health check
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/leads")
def create_lead(payload: LeadWrapper, db: Session = Depends(get_db)):
    try:
        lead_data = payload.getUserData
        normalized = utils.normalized_phone(lead_data.phone)
        
        lead = Lead(
            name=lead_data.name,
            phone=lead_data.phone,
            normalized_phone=normalized,
            preferred_start=lead_data.preferred_start,
            preferred_end=lead_data.preferred_end,
            reason=lead_data.reason
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        return {"status": "ok", "id": lead.id}
    except Exception as e:
        logger.exception("Error creating lead")
        raise HTTPException(status_code=500, detail=str(e))

#TEST RESPONSE
# @app.post("/v1/leads")
# async def create_lead(request: Request, db: Session = Depends(get_db)):
#     data = await request.json()
#     logger.info("Raw payload: %s", data)
#     return {"received": data}

# List all leads
@app.get("/v1/leads", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.id.desc()).all()
    return [LeadOut.from_orm(l) for l in leads]
