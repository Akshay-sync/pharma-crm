# Pharma CRM – AI-First HCP Interaction Logger

A full-stack AI-powered CRM system for logging and managing Healthcare Professional (HCP) interactions using natural language chat.

## Tech Stack

- **Frontend:** React + Vite (branch: `frontend`)
- **Backend:** Python + FastAPI (branch: `main`)
- **AI Framework:** LangGraph + Groq (llama-3.3-70b-versatile)
- **Database:** PostgreSQL

## Features

- Log HCP interactions via natural language chat
- AI automatically fills the form from chat input
- Edit interactions by telling the AI what to change
- Get HCP profile and interaction history
- AI-suggested follow-up actions
- Free-text summarization into structured fields

## LangGraph Tools (5)

1. `log_interaction` – Logs a new HCP interaction with AI summary
2. `edit_interaction` – Edits specific fields of an existing interaction
3. `get_hcp_details` – Fetches HCP profile and past interaction history
4. `suggest_followup` – Suggests 3 next steps based on last interaction
5. `summarize_interaction` – Extracts structured data from free-text notes

## Setup Instructions

### Backend
```bash
cd pharma-crm-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd pharma-crm-frontend
npm install
npm run dev
```

### Environment Variables
Create a `.env` file in the backend folder:
```
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://username:password@localhost/pharma_crm
```
