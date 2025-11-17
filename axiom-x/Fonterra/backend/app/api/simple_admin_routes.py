from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

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

# Chatbot service
class AnthropicChatbot:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.api_available = bool(self.api_key)
        if not self.api_available:
            print("  ANTHROPIC_API_KEY not found - using demo mode")

    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None,
                   conversation_history: Optional[List[ChatMessage]] = None) -> ChatResponse:
        if not self.api_available:
            return await self._demo_response(message, context)
        
        # Real API call would go here
        return ChatResponse(
            response="API key configured - real Claude response would go here",
            timestamp=datetime.utcnow(),
            model_used="claude-haiku-4-5-20251001",
            tokens_used=50
        )

    async def _demo_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> ChatResponse:
        response = f"Hello! I am the CKICAS dashboard assistant. You asked: '{message}'. I'm currently in demo mode without an Anthropic API key, but I can help you understand the dashboard metrics and system performance."
        return ChatResponse(
            response=response,
            timestamp=datetime.utcnow(),
            model_used="demo_mode",
            tokens_used=0
        )

chatbot = AnthropicChatbot()

@router.get("/health")
async def admin_health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": ["database", "cache", "api"]
    }

@router.get("/metrics")
async def get_system_metrics():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cache": {"hit_rate": 0.85, "entries": 150},
        "api_performance": {"avg_response_time": 0.15, "requests_per_hour": 120}
    }

@router.post("/chat", response_model=ChatResponse)
async def chat_with_dashboard(request: ChatRequest):
    try:
        response = await chatbot.chat(
            message=request.message,
            context=request.context,
            conversation_history=request.conversation_history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@router.get("/chat/health")
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
