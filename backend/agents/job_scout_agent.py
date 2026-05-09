from groq import Groq
import os
import json
from dotenv import load_dotenv
from rag.embeddings import extract_cv_info
from agents.tools import search_jobs, generate_search_queries

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def score_job(job: dict, cv_info: dict) -> dict:
    
    prompt = """
    Tum ek career expert ho. Neeche ek job aur candidate ki profile hai.
    Job ko candidate ke liye 0-100 score do aur short reasoning likho.
    
    Candidate Skills: """ + str(cv_info.get('skills', [])) + """
    Experience: """ + str(cv_info.get('experience_years', 0)) + """ years
    Previous Titles: """ + str(cv_info.get('job_titles', [])) + """
    Education: """ + str(cv_info.get('education', '')) + """
    
    Job Title: """ + str(job.get('title', '')) + """
    Job Description: """ + str(job.get('description', ''))[:300] + """
    
    Sirf JSON return karo:
    {"score": 85, "reasoning": "Strong match because...", "missing_skills": ["skill1"]}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    try:
        result = response.choices[0].message.content
        result = result.replace("```json", "").replace("```", "").strip()
        scored_data = json.loads(result)
        return {**job, **scored_data}
    except:
        return {**job, "score": 50, "reasoning": "Match evaluated", "missing_skills": []}

def run_agent(cv_text: str, session_id: str) -> dict:
    
    print("Agent starting for session: " + session_id)
    
    print("Step 1: CV analyze ho rahi hai...")
    cv_info = extract_cv_info(cv_text)
    
    print("Step 2: Search queries ban rahi hain...")
    queries = generate_search_queries(cv_info)
    
    print("Step 3: Jobs search ho rahi hain...")
    all_jobs = []
    for query in queries:
        jobs = search_jobs(query)
        all_jobs.extend(jobs)
    
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        if job['url'] not in seen:
            seen.add(job['url'])
            unique_jobs.append(job)
    
    print("Step 4: Jobs score ho rahi hain...")
    scored_jobs = []
    for job in unique_jobs[:10]:
        scored_job = score_job(job, cv_info)
        scored_jobs.append(scored_job)
    
    scored_jobs.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    print("Agent complete! " + str(len(scored_jobs)) + " jobs mili hain!")
    
    return {
        "session_id": session_id,
        "cv_info": cv_info,
        "jobs": scored_jobs,
        "total_jobs": len(scored_jobs)
    }