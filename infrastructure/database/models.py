from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    category = Column(String(50))
    metadata_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobOfferModel(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(String(50), unique=True, index=True)
    title = Column(String(200))
    description = Column(String(1000), nullable=True)
    industry = Column(String(100), nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow)

class ProgramModel(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(500), nullable=True)
    skills = Column(JSON)  # Store skills as a list of strings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
