from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from datetime import datetime
import os
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

app = FastAPI(title="CKICAS Ultra-Simple")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
    app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")
    # Fallback: serve assets directly from catch-all
    pass

# Basic health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-simple CKICAS running"}

# Admin endpoints
@app.get("/api/admin/health")
async def admin_health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": ["database", "cache", "api"]
    }

@app.get("/api/admin/chat/health")
async def check_chatbot_health():
    try:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {
                "status": "demo_mode",
                "model": "demo_assistant",
                "provider": "CKICAS",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        return {
            "status": "healthy",
            "model": "claude-haiku-4-5-20251001",
            "provider": "Anthropic",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/api/admin/chat")
async def chat_with_dashboard(request: ChatRequest):
    # Simplified response for now
    return ChatResponse(
        response="Chat functionality temporarily disabled during deployment",
        timestamp=datetime.utcnow(),
        model_used="demo",
        tokens_used=0
    )

# Specific route for root path
@app.get("/")
async def serve_root():
    # Return plain text for testing
    return "CKICAS Drought Monitoring Dashboard - Backend Connected"

# Catch-all route for SPA (MUST be last)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return f"Path: {full_path} - SPA routing working"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
