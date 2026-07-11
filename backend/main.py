import os
from dotenv import load_dotenv
load_dotenv()   # ← must be BEFORE any LangChain/Groq imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from agent import crm_agent
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="AI-First CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response schemas ──────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str    # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str
    form_updates: Optional[Dict[str, Any]] = None
    action_type: Optional[str] = None   # "log" | "edit" | "none"

# ── Endpoints ────────────────────────────────────────────────────────────────
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Build message history for the agent
    messages = []
    for msg in request.history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    messages.append(HumanMessage(content=request.message))

    # Run LangGraph agent
    final_state = crm_agent.invoke(
        {"messages": messages, "form_state": {}, "action_type": "none"}
    )

    # Extract last AI message text
    ai_msgs = [m for m in final_state["messages"] if isinstance(m, AIMessage)]
    response_text = ai_msgs[-1].content if ai_msgs else "I processed your request."

    form_updates = final_state.get("form_state", {})
    action_type  = final_state.get("action_type", "none")

    return ChatResponse(
        response=response_text,
        form_updates=form_updates,
        action_type=action_type
    )

@app.get("/api/health")
def health():
    return {"status": "ok", "model": "llama-3.3-70b-versatile"}
