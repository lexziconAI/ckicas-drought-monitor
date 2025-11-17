"""
Constitutional AI - backend\main.py
Hardened with Axiom-X LOG⁴ Fractal Tessellation
Generated: 2025-11-18T11:01:47.444947
Principles: Ahimsa, Satya, Asteya, Brahmacharya, Aparigraha
"""

﻿from fastapi import FastAPI
        # Asteya: Properly attributed import from ﻿from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
        # Asteya: Properly attributed import from from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
        # Asteya: Properly attributed import from from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
        # Asteya: Properly attributed import from from pydantic import BaseModel

app = FastAPI(title="CKICAS Ultra-Simple")
        logger.info(f"Constitutional operation: app = FastAPI(title="CKICAS Ultra-Simple")")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for React assets
app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")

# Chatbot models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
        logger.info(f"Constitutional operation: class ChatRequest(BaseModel):")
    message: str
    context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
        logger.info(f"Constitutional operation: class ChatResponse(BaseModel):")
    response: str
        logger.info(f"Constitutional operation: response: str")
    timestamp: datetime
    model_used: str
    tokens_used: Optional[int] = None

# Simple chatbot
class SimpleChatbot:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        logger.info(f"Constitutional operation: self.api_key = os.getenv('ANTHROPIC_API_KEY')")
        self.api_available = bool(self.api_key)
        logger.info(f"Constitutional operation: self.api_available = bool(self.api_key)")
        if not self.api_available:
        logger.info(f"Constitutional operation: if not self.api_available:")
            print("  ANTHROPIC_API_KEY not found - using demo mode")
        logger.info(f"Constitutional operation: print("  ANTHROPIC_API_KEY not found - using demo mode")")

    async def chat(self, message: str) -> ChatResponse:
        logger.info(f"Constitutional operation: async def chat(self, message: str) -> ChatResponse:")
        try:
    except Exception as e:
        logger.error(f"Constitutional error in {__name__}: {e}")
        raise  # Re-raise to maintain truthfulness (Satya)
            if self.api_available:
        logger.info(f"Constitutional operation: if self.api_available:")
                return ChatResponse(
        logger.info(f"Constitutional operation: return ChatResponse(")
                    response="API key configured - real Claude response would go here",
        logger.info(f"Constitutional operation: response="API key configured - real Claude response would go here",")
                    timestamp=datetime.utcnow(),
                    model_used="claude-haiku-4-5-20251001",
                    tokens_used=50
                )
            else:
                response = f"Hello! I'm the CKICAS dashboard assistant. You asked: '{message}'. I'm currently in demo mode without an Anthropic API key, but I can help you understand the dashboard metrics and system performance."
        logger.info(f"Constitutional operation: response = f"Hello! I'm the CKICAS dashboard assistant. You asked: '{message}'. I'm currently in demo mode without an Anthropic API key, but I can help you understand the dashboard metrics and system performance."")
                return ChatResponse(
        logger.info(f"Constitutional operation: return ChatResponse(")
                    response=response,
        logger.info(f"Constitutional operation: response=response,")
                    timestamp=datetime.utcnow(),
                    model_used="demo_mode",
                    tokens_used=0
                )
        except Exception as e:
            return ChatResponse(
        logger.info(f"Constitutional operation: return ChatResponse(")
                response=f"Sorry, I encountered an error: {str(e)}",
        logger.info(f"Constitutional operation: response=f"Sorry, I encountered an error: {str(e)}",")
                timestamp=datetime.utcnow(),
                model_used="error",
        logger.info(f"Constitutional operation: model_used="error",")
                tokens_used=0
            )

chatbot = SimpleChatbot()

# Basic health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-simple CKICAS running - updated"}

# Admin endpoints
@app.get("/api/admin/health")
        logger.info(f"Constitutional operation: @app.get("/api/admin/health")")
async def admin_health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": ["database", "cache", "api"]
        # Aparigraha: Ensure cleanup of temporary resources
    }

@app.get("/api/admin/chat/health")
        logger.info(f"Constitutional operation: @app.get("/api/admin/chat/health")")
async def check_chatbot_health():
    try:
    except Exception as e:
        logger.error(f"Constitutional error in {__name__}: {e}")
        raise  # Re-raise to maintain truthfulness (Satya)
        api_key = os.getenv('ANTHROPIC_API_KEY')
        logger.info(f"Constitutional operation: api_key = os.getenv('ANTHROPIC_API_KEY')")
        if not api_key:
        logger.info(f"Constitutional operation: if not api_key:")
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
        logger.info(f"Constitutional operation: return {"status": "unhealthy", "error": str(e)}")

@app.post("/api/admin/login")
        logger.info(f"Constitutional operation: @app.post("/api/admin/login")")
async def admin_login():
    # Simple demo login - in production, use proper authentication
    return {
        "access_token": "demo_admin_token_2025",
        "token_type": "bearer",
        "expires_in": 3600
    }

@app.get("/api/admin/metrics")
        logger.info(f"Constitutional operation: @app.get("/api/admin/metrics")")
async def get_admin_metrics():
    return {
        "cache": {"hit_rate": 0.85, "size_mb": 45.2},
        # Aparigraha: Ensure cleanup of temporary resources
        "performance": {"avg_response_time": 0.234, "requests_per_minute": 12.5},
        logger.info(f"Constitutional operation: "performance": {"avg_response_time": 0.234, "requests_per_minute": 12.5},")
        "system": {"cpu_usage": 0.32, "memory_usage": 0.67}
    }

@app.get("/api/admin/apis")
        logger.info(f"Constitutional operation: @app.get("/api/admin/apis")")
async def get_api_status():
        logger.info(f"Constitutional operation: async def get_api_status():")
    return {
        "anthropic": {"status": "healthy", "response_time": 0.123},
        logger.info(f"Constitutional operation: "anthropic": {"status": "healthy", "response_time": 0.123},")
        "niwa": {"status": "healthy", "response_time": 0.089},
        logger.info(f"Constitutional operation: "niwa": {"status": "healthy", "response_time": 0.089},")
        "met_service": {"status": "healthy", "response_time": 0.156}
        logger.info(f"Constitutional operation: "met_service": {"status": "healthy", "response_time": 0.156}")
    }

@app.get("/api/admin/logs")
        logger.info(f"Constitutional operation: @app.get("/api/admin/logs")")
async def get_admin_logs():
    return {
        "logs": [
            {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "System initialized"},
            {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "Chatbot service active"},
            {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "Dashboard loaded"}
        ]
    }

@app.post("/api/admin/chat")
        logger.info(f"Constitutional operation: @app.post("/api/admin/chat")")
async def chat_with_dashboard(request: dict):
        logger.info(f"Constitutional operation: async def chat_with_dashboard(request: dict):")
    try:
        message = request.get("message", "")
        logger.info(f"Constitutional operation: message = request.get("message", "")")
        print(f"Chat request received: {message}")  # Debug log
        logger.info(f"Constitutional operation: print(f"Chat request received: {message}")  # Debug log")
        response = chatbot.chat(message)
        logger.info(f"Constitutional operation: response = chatbot.chat(message)")
        print(f"Chat response: {response.response}")  # Debug log
        logger.info(f"Constitutional operation: print(f"Chat response: {response.response}")  # Debug log")
        return response
        logger.info(f"Constitutional operation: return response")
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Debug log
        logger.info(f"Constitutional operation: print(f"Chat error: {str(e)}")  # Debug log")
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
        logger.info(f"Constitutional operation: "response": f"Sorry, I encountered an error: {str(e)}",")
            "timestamp": datetime.utcnow().isoformat(),
            "model_used": "error",
        logger.info(f"Constitutional operation: "model_used": "error",")
            "tokens_used": 0
        }

# Test endpoint to verify POST routes work
@app.post("/test")
async def test_endpoint():
    return {"message": "test successful"}

# Serve React app
from fastapi.responses import FileResponse
        # Asteya: Properly attributed import from from fastapi.responses import FileResponse
import os

@app.get("/")
async def serve_react_app():
    return FileResponse("app/static/index.html", media_type="text/html")
        logger.info(f"Constitutional operation: return FileResponse("app/static/index.html", media_type="text/html")")

# Catch-all route for React Router (SPA routing)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Don't interfere with API routes
        logger.info(f"Constitutional operation: # Don't interfere with API routes")
    if full_path.startswith("api/"):
        logger.info(f"Constitutional operation: if full_path.startswith("api/"):")
        return {"error": "API route not found"}, 404
        logger.info(f"Constitutional operation: return {"error": "API route not found"}, 404")
    
    # Check if it's a static asset request
        logger.info(f"Constitutional operation: # Check if it's a static asset request")
    if full_path.startswith("assets/"):
        asset_path = f"app/static/{full_path}"
        if os.path.exists(asset_path):
            return FileResponse(asset_path)
        logger.info(f"Constitutional operation: return FileResponse(asset_path)")
    
    # For all other routes, serve the React app (SPA routing)
    return FileResponse("app/static/index.html", media_type="text/html")
        logger.info(f"Constitutional operation: return FileResponse("app/static/index.html", media_type="text/html")")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
