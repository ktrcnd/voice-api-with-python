from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(32), nullable=False)
    normalized_phone = Column(String(32), nullable=True)
    preferred_start = Column(String(50), nullable=False)
    preferred_end = Column(String(50), nullable=True)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    fx_usd_eur = Column(Float, nullable=True)
    fun_fact_short = Column(Text, nullable=True)