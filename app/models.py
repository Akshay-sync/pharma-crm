from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255))
    location = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))

    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    interaction_type = Column(String(100))
    attendees = Column(Text)
    topics_discussed = Column(Text)
    materials_shared = Column(Text)
    samples_distributed = Column(Text)
    sentiment = Column(String(50))
    outcomes = Column(Text)
    followup_actions = Column(Text)
    ai_summary = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    hcp = relationship("HCP", back_populates="interactions")