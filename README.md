# 🤖 JobScout AI — Autonomous Job Hunting Agent

> Built for SMIT Agentic AI Hackathon | Muhammad Noraiz

## 🚀 Live Demo
- Frontend: (Vercel link — baad mein add karein)
- Backend: (Hugging Face link — baad mein add karein)

## 📌 What is JobScout AI?
JobScout AI is a fully autonomous career agent that:
1. Accepts your CV (PDF or Word)
2. Extracts your skills, experience, and education using AI
3. Autonomously searches real-time job listings
4. Scores each job against your profile (0-100%)
5. Explains WHY each job is a strong or weak match
6. Lets you chat with an AI Career Advisor about your CV

## 🧠 Agentic Workflow
CV Upload → Parse & Extract → Generate Queries → Search Jobs → Score & Rank → Display Results → Chat

## ⚙️ Tech Stack
| Layer | Technology |
|---|---|
| LLM | Groq (Llama 3.3 70B) |
| Agent | LangChain + LangGraph |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas |
| Job Search | Tavily API |
| Frontend | Next.js + Tailwind CSS |
| Backend Deploy | Hugging Face Spaces |
| Frontend Deploy | Vercel |

## 📁 Project Structure
```
jobscout-ai/
├── backend/
│   ├── main.py
│   ├── agents/
│   │   ├── job_scout_agent.py
│   │   └── tools.py
│   ├── rag/
│   │   ├── cv_parser.py
│   │   └── embeddings.py
│   ├── api/
│   │   └── routes.py
│   └── database/
│       └── mongo.py
└── frontend/
    └── app/
        └── page.tsx
```

## 🛠️ Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
MONGODB_URL=your_mongodb_url
```

Run:
```bash
python -m uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## ✨ Features
- ✅ CV Upload (PDF + Word)
- ✅ AI-powered skill extraction
- ✅ Real-time job search (LinkedIn, Indeed, Rozee.pk)
- ✅ Smart job scoring (0-100%)
- ✅ AI reasoning per job
- ✅ Filter by match strength
- ✅ Career Advisor Chat
- ✅ MongoDB session storage

## 🔑 Environment Variables
| Variable | Description |
|---|---|
| GROQ_API_KEY | Groq LLM API key |
| TAVILY_API_KEY | Tavily search API key |
| MONGODB_URL | MongoDB Atlas connection string |