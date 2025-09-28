from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timedelta, timezone
import re

class LeadCreate(BaseModel):
    name: str
    phone: str
    preferred_start: str
    preferred_end: Optional[str] = None
    reason: str = Field(..., min_length=5, max_length=200)
    utc_offset: Optional[str] = None
    call_id: Optional[str] = None

    @validator("name")
    def name_must_be_two_words(cls, v):
        if len(v.strip()) < 3 or len(v.split()) < 2:
            raise ValueError("name must be at least two words and greater than 3 characters")
        return v.strip()
    
    @validator("phone")
    def phone_must_be_digits(cls, v):
        digits = re.sub(r"\D", "", v)
        if not (10 <= len(digits) <= 15):
            raise ValueError("Phone must have 10 - 15 digits")
        return v
    
    @validator("preferred_start")
    def start_must_be_iso_and_48hours_future(cls, v):
        try:
            # parse ISO-8601 and make aware
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
        except Exception:
            raise ValueError("Preferred Start must follow the 'ISO-8601' date and time format")
        
        # current UTC aware datetime
        now = datetime.now(timezone.utc)

        # must be at least 48 hours in the future
        if dt <= now + timedelta(hours=48):
            raise ValueError("Preferred Start must be at least 48 hours in the future")
        
        return v
    
    @validator("preferred_end")
    def end_after_start(cls, v, values):
        if v is None:
            return v
        
        try:
            end_dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            start = values.get("preferred_start")
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        except Exception:
            raise ValueError("Preferred End must follow ISO-8601 format and be after preferred start")

        if end_dt <= start_dt:
            raise ValueError("Preferred End must be after preferred start")
        
        return v
    
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
