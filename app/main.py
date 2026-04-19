from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, get_db
from app.models import HCP, Interaction
from app.schemas import InteractionCreate, InteractionUpdate, InteractionResponse, HCPResponse, ChatRequest, ChatResponse
from app.agent import agent_executor

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pharma CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hcps", response_model=List[HCPResponse])
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()

@app.post("/interactions", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    db_interaction = Interaction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@app.put("/interactions/{id}", response_model=InteractionResponse)
def update_interaction(id: int, interaction: InteractionUpdate, db: Session = Depends(get_db)):
    db_interaction = db.query(Interaction).filter(Interaction.id == id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    update_data = interaction.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_interaction, key, value)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@app.get("/interactions/{hcp_id}", response_model=List[InteractionResponse])
def get_interactions(hcp_id: int, db: Session = Depends(get_db)):
    return db.query(Interaction).filter(Interaction.hcp_id == hcp_id).all()

@app.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    try:
        from app.agent import llm, summarize_interaction, suggest_followup, get_hcp_details
        
        message = request.message.lower()
        
        if "suggest" in message or "follow" in message:
            name = "Dr. Smith"
            result = suggest_followup.invoke({"hcp_name": name})
        elif "details" in message or "profile" in message:
            result = get_hcp_details.invoke({"hcp_name": "Dr. Smith"})
        else:
            result = summarize_interaction.invoke({"free_text": request.message})
        
        return {"response": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))