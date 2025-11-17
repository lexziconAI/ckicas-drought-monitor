from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CKICAS Ultra-Simple")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-simple CKICAS running"}

# Root endpoint
@app.get("/")
async def serve_root():
    return "CKICAS Drought Monitoring Dashboard - Backend Connected"

# Catch-all route
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return f"Path: {full_path} - SPA routing working"
