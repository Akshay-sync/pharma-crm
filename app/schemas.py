from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class HCPResponse(HCPBase):
    id: int
    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    hcp_id: int
    date: date
    time: time
    interaction_type: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    followup_actions: Optional[str] = None

class InteractionCreate(BaseModel):
    hcp_name: Optional[str] = None
    hcp_id: Optional[int] = None
    date: Optional[date] = None
    time: Optional[time] = None
    interaction_type: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    followup_actions: Optional[str] = None

class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    followup_actions: Optional[str] = None

class InteractionResponse(InteractionBase):
    id: int
    ai_summary: Optional[str] = None
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str