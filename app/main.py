from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import models so tables are registered
from app.models import candidate, education, job_description, score

# Import routers
from app.api.resume_routes import router as resume_router
from app.api.ranking_routes import router as ranking_router
from app.api.job_routes import router as job_router
from app.api.analytics_routes import router as analytics_router
from app.api.candidate_routes import router as candidate_router
from app.api.dashboard_routes import router as dashboard_router

app = FastAPI(title="HireSense AI Backend")

# -----------------------------
# CORS Configuration
# -----------------------------




origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://hiresense-ai-lac.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register routers
# -----------------------------
app.include_router(job_router)
app.include_router(resume_router)
app.include_router(ranking_router)
app.include_router(candidate_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "HireSense AI Backend is running"}