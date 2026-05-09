from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = MongoClient(MONGODB_URL)
db = client["jobscout"]

# Collections
cv_collection = db["cvs"]
results_collection = db["results"]
sessions_collection = db["sessions"]

def get_db():
    return db
