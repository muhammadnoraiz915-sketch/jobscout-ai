
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_jobs(query: str) -> list:
    """Tavily se real-time jobs search karta hai"""
    try:
        results = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_domains=[
                "linkedin.com",
                "rozee.pk",
                "indeed.com",
                "glassdoor.com",
                "mustakbil.com"
            ]
        )
        
        jobs = []
        for r in results.get("results", []):
            jobs.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "description": r.get("content", "")[:500],
                "source": r.get("url", "").split("/")[2] if r.get("url") else ""
            })
        return jobs
    except Exception as e:
        print(f"Search error: {e}")
        return []

def generate_search_queries(cv_info: dict) -> list:
    """CV info se search queries banata hai"""
    queries = []
    
    skills = cv_info.get("skills", [])[:3]
    titles = cv_info.get("job_titles", [])[:2]
    
    for title in titles:
        queries.append(f"{title} jobs Pakistan 2024")
        queries.append(f"{title} remote jobs")
    
    if skills:
        skill_str = " ".join(skills[:3])
        queries.append(f"{skill_str} developer jobs")
    
    if not queries:
        queries = ["software developer jobs Pakistan", "IT jobs Pakistan 2024"]
    
    return queries[:4]  # Max 4 queries