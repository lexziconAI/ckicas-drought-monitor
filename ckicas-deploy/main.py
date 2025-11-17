from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import os

print("Starting CKICAS application...")

app = FastAPI(title="CKICAS Ultra-Simple")

print("FastAPI app created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS middleware added")

# Mount static files for React assets
# app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# Chatbot models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    model_used: str
    tokens_used: Optional[int] = None

# Simple chatbot
class SimpleChatbot:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.api_available = bool(self.api_key)
        if not self.api_available:
            print("  ANTHROPIC_API_KEY not found - using demo mode")

    def chat(self, message: str):
        try:
            if self.api_available:
                return ChatResponse(
                    response="API key configured - real Claude response would go here",
                    timestamp=datetime.utcnow(),
                    model_used="claude-haiku-4-5-20251001",
                    tokens_used=50
                )
            else:
                response = f"Hello! I am the CKICAS dashboard assistant. You asked: '{message}'. I'm currently in demo mode without an Anthropic API key, but I can help you understand the dashboard metrics and system performance."
                return ChatResponse(
                    response=response,
                    timestamp=datetime.utcnow(),
                    model_used="demo_mode",
                    tokens_used=0
                )
        except Exception as e:
            return ChatResponse(
                response=f"Sorry, I encountered an error: {str(e)}",
                timestamp=datetime.utcnow(),
                model_used="error",
                tokens_used=0
            )

chatbot = SimpleChatbot()

# Basic health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "CKICAS running - FAST DEPLOY TEST"}

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

# Chat endpoint for both admin and main dashboard
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = chatbot.chat(request.message)
        return response
    except Exception as e:
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            timestamp=datetime.utcnow(),
            model_used="error",
            tokens_used=0
        )

# Serve React app
@app.get("/")
async def serve_react_app():
    return FileResponse("frontend/dist/index.html", media_type="text/html")

@app.get("/assets/{file_path:path}")
async def serve_asset(file_path: str):
    asset_path = f"frontend/dist/assets/{file_path}"
    print(f"DEBUG: Serving asset request: {file_path} -> {asset_path}")
    print(f"DEBUG: File exists: {os.path.exists(asset_path)}")
    
    if os.path.exists(asset_path):
        # Set correct MIME type based on file extension
        if file_path.endswith('.js'):
            print(f"DEBUG: Serving JS file with application/javascript MIME type")
            return FileResponse(asset_path, media_type="application/javascript")
        elif file_path.endswith('.css'):
            print(f"DEBUG: Serving CSS file with text/css MIME type")
            return FileResponse(asset_path, media_type="text/css")
        else:
            print(f"DEBUG: Serving file with default MIME type")
            return FileResponse(asset_path)
    
    print(f"DEBUG: Asset not found: {asset_path}")
    return {"error": "Asset not found"}, 404

# Catch-all route for React Router (SPA routing)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Don't interfere with API routes or asset routes
    if full_path.startswith("api/") or full_path.startswith("assets/"):
        return {"error": "Route not found"}, 404
    
    # For all other routes, serve the React app (SPA routing)
    return FileResponse("frontend/dist/index.html", media_type="text/html")
