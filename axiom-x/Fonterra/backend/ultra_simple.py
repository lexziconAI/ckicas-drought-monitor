from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Basic health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-simple CKICAS running"}

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

    async def chat(self, message: str) -> ChatResponse:
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

chatbot = SimpleChatbot()

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
    try:
        response = await chatbot.chat(request.message)
        return response
    except Exception as e:
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            timestamp=datetime.utcnow(),
            model_used="error",
            tokens_used=0
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
