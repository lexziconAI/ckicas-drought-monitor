from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

app = FastAPI(title="CKICAS Ultra-Simple")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for React assets
app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")

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

@app.post("/api/admin/login")
async def admin_login():
    # Simple demo login - in production, use proper authentication
    return {
        "access_token": "demo_admin_token_2025",
        "token_type": "bearer",
        "expires_in": 3600
    }

@app.get("/api/admin/metrics")
async def get_admin_metrics():
    return {
        "cache": {"hit_rate": 0.85, "size_mb": 45.2},
        "performance": {"avg_response_time": 0.234, "requests_per_minute": 12.5},
        "system": {"cpu_usage": 0.32, "memory_usage": 0.67}
    }

@app.get("/api/admin/apis")
async def get_api_status():
    return {
        "anthropic": {"status": "healthy", "response_time": 0.123},
        "niwa": {"status": "healthy", "response_time": 0.089},
        "met_service": {"status": "healthy", "response_time": 0.156}
    }

@app.get("/api/admin/logs")
async def get_admin_logs():
    return {
        "logs": [
            {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "System initialized"},
            {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "Chatbot service active"},
            {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "Dashboard loaded"}
        ]
    }

@app.post("/api/admin/chat")
async def chat_with_dashboard(request: ChatRequest):
    try:
        print(f"Chat request received: {request.message}")  # Debug log
        response = await chatbot.chat(request.message)
        print(f"Chat response: {response.response}")  # Debug log
        return response
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Debug log
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            timestamp=datetime.utcnow(),
            model_used="error",
            tokens_used=0
        )

# Serve React app
from fastapi.responses import FileResponse
import os

@app.get("/")
async def serve_react_app():
    return FileResponse("app/static/index.html", media_type="text/html")

# Catch-all route for React Router (SPA routing)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Don't interfere with API routes
    if full_path.startswith("api/"):
        return {"error": "API route not found"}, 404
    
    # Check if it's a static asset request
    if full_path.startswith("assets/"):
        asset_path = f"app/static/{full_path}"
        if os.path.exists(asset_path):
            return FileResponse(asset_path)
    
    # For all other routes, serve the React app (SPA routing)
    return FileResponse("app/static/index.html", media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
