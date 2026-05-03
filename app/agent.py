import os
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from app.database import SessionLocal
from app.models import Interaction, HCP

load_dotenv()

llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

@tool
def log_interaction(hcp_name: str, topics_discussed: str, sentiment: str, outcomes: str, followup_actions: str) -> str:
    """Logs a new HCP interaction to the database with an AI summary."""
    try:
        summary_prompt = f"Summarize: Topics: {topics_discussed}, Outcomes: {outcomes}, Follow-up: {followup_actions}"
        ai_summary = llm.invoke(summary_prompt).content
        db = SessionLocal()
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        hcp_id = hcp.id if hcp else 1
        from datetime import date, time
        new_interaction = Interaction(
            hcp_id=hcp_id, date=date.today(), time=time(12, 0),
            interaction_type="Meeting", topics_discussed=topics_discussed,
            sentiment=sentiment, outcomes=outcomes,
            followup_actions=followup_actions, ai_summary=ai_summary
        )
        db.add(new_interaction)
        db.commit()
        db.close()
        return f"Interaction logged! Summary: {ai_summary}"
    except Exception as e:
        return f"Error logging: {str(e)}"

@tool
def edit_interaction(interaction_id: str, field_name: str, new_value: str) -> str:    
    """Edits a specific field of an existing interaction."""
    try:
        db = SessionLocal()
        interaction_id = int(interaction_id)
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return "Interaction not found."
        setattr(interaction, field_name, new_value)
        db.commit()
        db.close()
        return f"Updated {field_name} to '{new_value}' successfully."
    except Exception as e:
        return f"Error editing: {str(e)}"

@tool
def get_hcp_details(hcp_name: str) -> str:
    """Gets an HCP profile and interaction history by name."""
    try:
        db = SessionLocal()
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        if not hcp:
            return f"No HCP found with name {hcp_name}"
        interactions = db.query(Interaction).filter(Interaction.hcp_id == hcp.id).all()
        history = "\n".join([f"- {i.date}: {i.interaction_type} | {i.ai_summary}" for i in interactions])
        db.close()
        return f"HCP: {hcp.name}, Specialty: {hcp.specialty}\nHistory:\n{history or 'No past interactions.'}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def suggest_followup(hcp_name: str) -> str:
    """Suggests next steps based on last interaction with an HCP."""
    try:
        db = SessionLocal()
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        if not hcp:
            return "HCP not found."
        last = db.query(Interaction).filter(Interaction.hcp_id == hcp.id).order_by(Interaction.date.desc()).first()
        db.close()
        if not last:
            return "No previous interactions found."
        prompt = f"Suggest 3 follow-up actions for sales rep after meeting {hcp.name}. Topics: {last.topics_discussed}, Outcomes: {last.outcomes}"
        return llm.invoke(prompt).content
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def summarize_interaction(free_text: str) -> str:
    """Extracts structured interaction details from free-text notes."""
    try:
        prompt = f"""Extract these fields from the text and return as plain text with exact labels:
- HCP Name
- Date  
- Interaction Type
- Topics Discussed
- Materials Shared
- Sentiment (Positive/Neutral/Negative)
- Outcomes
- Follow-up Actions

Text: {free_text}"""
        return llm.invoke(prompt).content
    except Exception as e:
        return f"Error: {str(e)}"

tools = [log_interaction, edit_interaction, get_hcp_details, suggest_followup, summarize_interaction]
agent_executor = create_react_agent(llm, tools)