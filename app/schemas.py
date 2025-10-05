from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timedelta, timezone
import re

class LeadCreate(BaseModel):
    name: str
    phone: str
    preferred_start: datetime  # Changed to datetime for automatic ISO parsing
    preferred_end: Optional[datetime] = None
    reason: str = Field(..., min_length=5, max_length=200)
    utc_offset: Optional[str] = None
    call_id: Optional[str] = None

    # --- Validators ---

    @validator("name")
    def name_must_be_two_words(cls, v):
        if len(v.strip()) < 3 or len(v.split()) < 2:
            raise ValueError("Name must be at least two words and greater than 3 characters")
        return v.strip()

    @validator("phone")
    def phone_must_be_digits(cls, v):
        digits = re.sub(r"\D", "", v)
        if not (10 <= len(digits) <= 15):
            raise ValueError("Phone must have 10 - 15 digits")
        return v

    @validator("preferred_start")
    def start_must_be_48_hours_future(cls, dt: datetime):
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:  # ensure tz-aware
            dt = dt.replace(tzinfo=timezone.utc)
        if dt <= now + timedelta(hours=48):
            raise ValueError("Appointment must be at least 48 hours in the future")
        return dt

    @validator("preferred_end")
    def end_after_start(cls, v: Optional[datetime], values):
        if v is None:
            return v

        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)

        start = values.get("preferred_start")
        if start is None:
            return v  # skip validation if start missing

        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)

        if v <= start:
            raise ValueError("Preferred end must be after preferred start")

        return v


# Wrapper for your payload
class LeadWrapper(BaseModel):
    getUserData: LeadCreate

class LeadOut(BaseModel):
    id: int
    name: str
    phone: str
    normalized_phone: Optional[str]
    preferred_start: str
    preferred_end: Optional[str]
    reason: str
    created_at: datetime
    fx_usd_eur: Optional[float]
    fun_fact_short: Optional[str]

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }
