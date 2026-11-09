import os
import json
from typing import TypedDict, Annotated, Optional
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.tools import tool

# ─────────────────────────────────────────────
#  STATE
# ─────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    form_state: dict
    action_type: str   # "log" | "edit" | "none"

# ─────────────────────────────────────────────
#  TOOL 1 – Log Interaction (MANDATORY)
# ─────────────────────────────────────────────
@tool
def log_interaction(
    hcp_name: str = "",
    interaction_type: str = "Meeting",
    date: str = "",
    time: str = "",
    attendees: str = "",
    topics: str = "",
    materials: str = "",
    samples: str = "",
    sentiment: str = "",
    outcomes: str = ""
) -> str:
    """
    Extracts interaction details from the user's natural language description
    and populates the CRM form fields.
    Use this when the user describes a NEW interaction with an HCP.
    Parameters map directly to form fields.
    """
    payload = {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "date": date,
        "time": time,
        "attendees": attendees,
        "topics": topics,
        "materials": materials,
        "samples": samples,
        "sentiment": sentiment,
        "outcomes": outcomes,
    }
    return json.dumps({"action": "log", "data": payload})

# ─────────────────────────────────────────────
#  TOOL 2 – Edit Interaction (MANDATORY)
# ─────────────────────────────────────────────
@tool
def edit_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    attendees: Optional[str] = None,
    topics: Optional[str] = None,
    materials: Optional[str] = None,
    samples: Optional[str] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up: Optional[str] = None
) -> str:
    """
    Modifies ONLY the specific fields that the user wants to correct in an already-logged interaction.
    Only provide fields that need to be changed; leave all others as None.
    Use this when the user says things like 'change', 'update', 'sorry it was actually', 'correct the'.
    """
    payload = {k: v for k, v in {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "date": date,
        "time": time,
        "attendees": attendees,
        "topics": topics,
        "materials": materials,
        "samples": samples,
        "sentiment": sentiment,
        "outcomes": outcomes,
        "follow_up": follow_up,
    }.items() if v is not None}
    return json.dumps({"action": "edit", "data": payload})

# ─────────────────────────────────────────────
#  TOOL 3 – Search HCP Database
# ─────────────────────────────────────────────
@tool
def search_hcp(hcp_name: str) -> str:
    """
    Searches the CRM database for a Healthcare Professional (HCP) by name.
    Returns their specialty, location, and ID if found.
    Use this to validate an HCP name or get more context before logging.
    """
    hcp_db = {
        "dr. smith":  {"id": "HCP001", "name": "Dr. Smith",  "specialty": "Cardiology",  "location": "New York, NY"},
        "dr. john":   {"id": "HCP002", "name": "Dr. John",   "specialty": "Neurology",   "location": "Boston, MA"},
        "dr. patel":  {"id": "HCP003", "name": "Dr. Patel",  "specialty": "Oncology",    "location": "Chicago, IL"},
        "dr. sharma": {"id": "HCP004", "name": "Dr. Sharma", "specialty": "Pediatrics",  "location": "Dallas, TX"},
    }
    match = hcp_db.get(hcp_name.strip().lower())
    if match:
        return f"HCP Found: {match['name']} | Specialty: {match['specialty']} | Location: {match['location']} | ID: {match['id']}"
    return f"No HCP found for '{hcp_name}'. The name will still be recorded as entered."

# ─────────────────────────────────────────────
#  TOOL 4 – Get Product Info
# ─────────────────────────────────────────────
@tool
def get_product_info(product_name: str) -> str:
    """
    Retrieves information about a specific pharmaceutical product by name.
    Returns efficacy data, approved indications, and available materials.
    Use this when the user mentions a product during an interaction to add context.
    """
    products = {
        "product x": {
            "full_name": "Product-X (Xtenza)",
            "indication": "Cardiovascular Disease Management",
            "efficacy": "94% efficacy in reducing LDL cholesterol in Phase 3 trials.",
            "materials": ["Clinical Efficacy Brochure", "Patient Guide", "Dosing Card"]
        },
        "prodo-x": {
            "full_name": "Prodo-X",
            "indication": "Cardiovascular conditions",
            "efficacy": "Highly efficacious for cardiovascular conditions. Efficacy rate 94%.",
            "materials": ["Prodo-X Brochure", "Efficacy Summary Sheet"]
        }
    }
    key = product_name.strip().lower()
    for pk, pv in products.items():
        if pk in key or key in pk:
            return (f"Product: {pv['full_name']} | Indication: {pv['indication']} | "
                    f"Efficacy: {pv['efficacy']} | Available Materials: {', '.join(pv['materials'])}")
    return f"No product info found for '{product_name}'."

# ─────────────────────────────────────────────
#  TOOL 5 – Suggest Follow-up Action
# ─────────────────────────────────────────────
@tool
def suggest_follow_up(sentiment: str, topics: str, hcp_name: str = "") -> str:
    """
    Analyzes the interaction sentiment and topics to generate a smart follow-up action recommendation.
    Populates the Follow-up Actions field on the form.
    Use this when the user asks for suggestions, or automatically after logging a positive/negative interaction.
    """
    s = sentiment.strip().lower()
    t = topics.strip().lower()
    name = hcp_name if hcp_name else "the HCP"

    if s == "positive":
        if "product" in t or "efficacy" in t or "brochure" in t:
            return f"✅ Follow-up: Schedule a product demo with {name} within 2 weeks. Send advanced clinical trial data via email. Flag as high-priority account."
        return f"✅ Follow-up: Send a thank-you email to {name} within 24 hours. Schedule next meeting in 30 days."
    elif s == "negative":
        return f"⚠️ Follow-up: Flag for manager review. Send clarifying literature addressing {name}'s concerns. Schedule a call with medical affairs team within 1 week."
    else:
        return f"ℹ️ Follow-up: Send standard follow-up email to {name} with product overview. Check in again in 2 weeks."

# ─────────────────────────────────────────────
#  LLM + GRAPH
# ─────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
tools = [log_interaction, edit_interaction, search_hcp, get_product_info, suggest_follow_up]
tools_by_name = {t.name: t for t in tools}

# Initialize Groq LLM - using instant model (separate token limit from versatile)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = SystemMessage(content="""You are an AI-First CRM Assistant for a Life Sciences company, helping field representatives log interactions with Healthcare Professionals (HCPs).

You control a read-only form on the LEFT side of the screen through your tools. NEVER tell the user to fill the form manually.

=== CRITICAL TOOL USAGE RULES ===

1. LOG_INTERACTION — Use when the user describes a NEW or first-time interaction.
   Extract ALL relevant fields you can from their message.

2. EDIT_INTERACTION — Use ONLY when the user is CORRECTING a previously logged interaction.
   IMPORTANT: Only pass the fields that are actually changing. Do NOT pass fields that remain the same.
   For example, if user says "the name was actually Dr. John and sentiment was negative",
   only pass hcp_name="Dr. John" and sentiment="Negative". Do NOT include date, topics, materials etc.

3. SEARCH_HCP — Use whenever an HCP name is mentioned, to look them up.

4. GET_PRODUCT_INFO — Use when the user mentions a drug or product name.

5. SUGGEST_FOLLOW_UP — Use when the interaction has a clear sentiment and topics to generate a follow-up recommendation.

=== FIELD EXTRACTION RULES ===
- hcp_name: Doctor or HCP name (e.g. "Dr. Smith")
- interaction_type: "Meeting", "Call", or "Email" (default "Meeting")
- date: If user says "today", leave as "today" — the frontend resolves it to today's date automatically
- time: Extract if mentioned, else leave blank
- attendees: Anyone else present besides the rep and HCP
- topics: Key medical or product topics discussed
- materials: Brochures or documents shared
- samples: Drug samples distributed
- sentiment: "Positive", "Negative", or "Neutral"
- outcomes: Key agreements or results from the meeting

Always confirm what actions you took in a brief, helpful response.
""")

def call_model(state: AgentState):
    msgs = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in msgs):
        msgs = [SYSTEM_PROMPT] + list(msgs)
    response = llm_with_tools.invoke(msgs)
    # Explicitly carry forward form_state and action_type so they are not lost
    # when LangGraph merges state after this node runs
    return {
        "messages": [response],
        "form_state": state.get("form_state", {}),
        "action_type": state.get("action_type", "none"),
    }

def call_tools(state: AgentState):
    last_message = state["messages"][-1]
    tool_responses = []
    form_updates = {}
    action_type = "none"

    for tc in last_message.tool_calls:
        tool_name = tc["name"]
        tool_args = tc["args"]
        tool_fn = tools_by_name.get(tool_name)

        if tool_fn is None:
            result = f"Tool '{tool_name}' not found."
            tool_responses.append(ToolMessage(content=result, tool_call_id=tc["id"], name=tool_name))
            continue

        result = tool_fn.invoke(tool_args)

        # For log/edit tools, parse the JSON result to extract form updates
        if tool_name in ("log_interaction", "edit_interaction"):
            try:
                parsed = json.loads(result)
                action_type = parsed.get("action", "log")
                form_updates = {**form_updates, **parsed.get("data", {})}
            except Exception:
                pass

        tool_responses.append(ToolMessage(content=result, tool_call_id=tc["id"], name=tool_name))

    return {
        "messages": tool_responses,
        "form_state": form_updates,
        "action_type": action_type
    }

def should_continue(state: AgentState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

# Build graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", call_tools)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
builder.add_edge("tools", "agent")
crm_agent = builder.compile()
