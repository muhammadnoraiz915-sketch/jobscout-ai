from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_cv_info(cv_text: str) -> dict:
    
    prompt = """
    Neeche ek CV ka text hai. Is se yeh information extract karo JSON format mein:
    - name: candidate ka naam
    - skills: list of technical and soft skills
    - experience_years: total years of experience (number)
    - job_titles: previous job titles list
    - education: highest education
    - location: candidate ki location
    - summary: 2-3 line ka professional summary
    
    Sirf JSON return karo, kuch aur mat likho.
    
    CV Text:
    """ + cv_text[:3000]
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    try:
        result = response.choices[0].message.content
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return {
            "raw_text": cv_text[:500],
            "skills": [],
            "experience_years": 0,
            "job_titles": [],
            "education": "",
            "location": "",
            "summary": ""
        }