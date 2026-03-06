from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import DB initializer
from app.init_db import init_db

# ML Model
from app.ml.model import embedding_model

# Routers
from app.api.resume_routes import router as resume_router
from app.api.ranking_routes import router as ranking_router
from app.api.job_routes import router as job_router
from app.api.analytics_routes import router as analytics_router
from app.api.candidate_routes import router as candidate_router
from app.api.dashboard_routes import router as dashboard_router


app = FastAPI(title="HireSense AI Backend")


# -----------------------------
# Startup Tasks
# -----------------------------
@app.on_event("startup")
def startup_event():

    # Initialize database
    init_db()

    # Preload embedding model
    embedding_model.load_model()

    print("Database initialized")
    print("Embedding model loaded")


# -----------------------------
# CORS
# -----------------------------
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://hiresense-ai-lac.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Routers
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