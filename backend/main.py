from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="JobScout AI",
    description="Autonomous Job Hunting Agent",
    version="1.0.0"
)

# CORS — frontend se connect hone ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes add karo
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "JobScout AI chal raha hai! 🤖"}
