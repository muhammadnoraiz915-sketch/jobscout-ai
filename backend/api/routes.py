from groq import Groq
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
from rag.cv_parser import parse_cv
from agents.job_scout_agent import run_agent
from database.mongo import results_collection, sessions_collection
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="Sirf PDF ya Word file upload karo!")
    
    session_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{session_id}_{file.filename}"
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    try:
        cv_text = parse_cv(file_path)
        
        if not cv_text or len(cv_text) < 50:
            raise HTTPException(status_code=400, detail="CV text nahi mila!")
        
        sessions_collection.insert_one({
            "session_id": session_id,
            "filename": file.filename,
            "status": "processing"
        })
        
        results = run_agent(cv_text, session_id)
        
        results_collection.insert_one({
            "session_id": session_id,
            **results
        })
        
        sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"status": "completed"}}
        )
        
        os.remove(file_path)
        
        return JSONResponse(content={
            "success": True,
            "session_id": session_id,
            "message": str(results['total_jobs']) + " jobs mili hain!",
            "data": results
        })
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{session_id}")
async def get_results(session_id: str):
    result = results_collection.find_one(
        {"session_id": session_id},
        {"_id": 0}
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Results nahi mile!")
    
    return JSONResponse(content={"success": True, "data": result})

@router.get("/health")
async def health():
    return {"status": "JobScout AI chal raha hai!"}

class ChatRequest(BaseModel):
    message: str
    cv_info: dict
    jobs: list

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    
    prompt = """
    Tum ek career counselor ho. Candidate ki CV info aur matched jobs dekh kar unke sawal ka jawab do.
    
    Candidate Info: """ + str(request.cv_info) + """
    
    Top Matched Jobs: """ + str(request.jobs[:3]) + """
    
    User ka sawal: """ + request.message + """
    
    Short, helpful aur friendly jawab do. Urdu ya English mein jo user ne likha ho.
    """
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return {"reply": response.choices[0].message.content}