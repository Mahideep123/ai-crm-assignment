# 🏥 AI-First CRM – HCP Log Interaction Module

An AI-powered CRM screen for Life Science field representatives to log interactions with Healthcare Professionals (HCPs) using natural language chat.

## 📸 Features
- **Split-screen UI**: Interaction form (left) + AI Assistant chat (right)
- **AI-controlled form**: You NEVER type into the form — the AI fills it for you
- **5 LangGraph tools**: log_interaction, edit_interaction, search_hcp, get_product_info, suggest_follow_up
- **Powered by**: LangGraph + Groq (`llama-3.3-70b-versatile`)

## 🛠 Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Redux Toolkit |
| Backend | Python FastAPI |
| AI Agent | LangGraph |
| LLM | Groq (`llama-3.3-70b-versatile`) |
| Database | SQLite (dev) / MySQL or PostgreSQL (prod) |
| Font | Google Inter |

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd ai-crm-assignment
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install fastapi uvicorn sqlalchemy langgraph langchain-groq pydantic python-dotenv
```

Create a `.env` file inside `backend/`:
```
GROQ_API_KEY=your_groq_api_key_here
# Optional: DATABASE_URL=mysql+pymysql://user:password@localhost/crmdb
```

Start the server:
```bash
uvicorn main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## 🤖 LangGraph Tools (5 Tools)

| # | Tool | Description |
|---|------|-------------|
| 1 | `log_interaction` | Extracts HCP name, date, topics, sentiment, materials etc. from natural language and populates the form |
| 2 | `edit_interaction` | Updates ONLY the fields the user wants to correct — leaves all others unchanged |
| 3 | `search_hcp` | Queries the CRM database to validate an HCP name and get their specialty/location |
| 4 | `get_product_info` | Retrieves efficacy data and available materials for a pharmaceutical product |
| 5 | `suggest_follow_up` | Generates a smart follow-up action based on sentiment and topics discussed |

## 💬 Example Prompts to Test

**Log a new interaction:**
> "Today I met with Dr. Smith and discussed Product X efficiency. The sentiment was positive and I shared the brochures."

**Edit a field:**
> "Sorry, the name was actually Dr. John, and the sentiment was negative."

**Get follow-up suggestion:**
> "Suggest a follow-up action based on the current interaction."

**Search HCP:**
> "Can you look up Dr. Patel in the database?"

**Get product info:**
> "What materials are available for Prodo-X?"
