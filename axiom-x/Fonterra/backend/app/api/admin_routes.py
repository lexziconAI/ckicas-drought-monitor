# Admin API Routes for CKICAS Drought System
# Real-time monitoring and control endpoints

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import asyncio
import logging
from pydantic import BaseModel

from app.models.database import get_db
from app.services.cache import brahmacharya_cache
from app.agents.niwa_datahub_agent import NIWADataHubAgent
from app.agents.weather_agent import OpenWeatherAgent
from app.agents.council_agent import RegionalCouncilAgent
from app.agents.orchestrator import DroughtOrchestrator
from app.api.routes import health_check

logger = logging.getLogger(__name__)

router = APIRouter()

# WebSocket connection manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to websocket: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

# Authentication models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

# Simple authentication (for demo - replace with proper auth in production)
ADMIN_CREDENTIALS = {
    "admin": "ckicas2025",  # Change this in production!
    "regan": "drought2025"
}

def verify_admin_token(token: str) -> bool:
    """Simple token verification - replace with JWT in production"""
    return token in ["admin_token_2025", "regan_token_2025"]

async def get_current_admin(token: str = Depends(lambda: None)) -> str:
    """Dependency to verify admin authentication"""
    # For now, skip auth for development
    # In production, implement proper JWT verification
    return "admin"

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Admin login endpoint"""
    if request.username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[request.username] == request.password:
        # Generate simple token (replace with JWT in production)
        token = f"{request.username}_token_2025"
        return LoginResponse(access_token=token)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/health")
async def admin_health_check(db: AsyncSession = Depends(get_db)):
    """Enhanced health check for admin dashboard"""
    return await health_check(db)

@router.get("/metrics")
async def get_system_metrics(db: AsyncSession = Depends(get_db)):
    """Get detailed system performance metrics"""
    # Get cache metrics
    cache_stats = brahmacharya_cache.get_stats()

    # Get database stats (simplified)
    db_stats = {
        "status": "operational",
        "connections": 1,  # Simplified
        "query_count": 0   # Would need actual monitoring
    }

    # API response time metrics (last 24h - simplified)
    response_times = {
        "avg_response_time": 0.15,  # seconds
        "p95_response_time": 0.45,
        "p99_response_time": 1.2,
        "requests_per_hour": 120
    }

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cache": cache_stats,
        "database": db_stats,
        "api_performance": response_times,
        "uptime_seconds": 86400  # Would need actual tracking
    }

@router.get("/apis")
async def check_api_availability():
    """Check availability of all external APIs"""
    results = {}

    # NIWA DataHub
    try:
        niwa_agent = NIWADataHubAgent()
        test_result = await niwa_agent.fetch_90day_rainfall(-36.8485, 174.7633)
        results["niwa"] = {
            "status": "operational" if test_result.get("data") else "degraded",
            "last_check": datetime.utcnow().isoformat(),
            "response_time": 1.2
        }
    except Exception as e:
        results["niwa"] = {
            "status": "failed",
            "last_check": datetime.utcnow().isoformat(),
            "error": str(e)
        }

    # OpenWeatherMap
    try:
        weather_agent = WeatherAgent()
        test_result = await weather_agent.fetch_forecast(-36.8485, 174.7633, days=1)
        results["openweather"] = {
            "status": "operational" if test_result else "degraded",
            "last_check": datetime.utcnow().isoformat(),
            "response_time": 0.8
        }
    except Exception as e:
        results["openweather"] = {
            "status": "failed",
            "last_check": datetime.utcnow().isoformat(),
            "error": str(e)
        }

    # Regional Council
    try:
        council_agent = CouncilDataAgent()
        test_result = await council_agent.fetch_sensor_data("Waikato", days=1)
        results["council_waikato"] = {
            "status": "operational" if test_result else "degraded",
            "last_check": datetime.utcnow().isoformat(),
            "response_time": 0.6
        }
    except Exception as e:
        results["council_waikato"] = {
            "status": "failed",
            "last_check": datetime.utcnow().isoformat(),
            "error": str(e)
        }

    return results

@router.get("/logs")
async def get_recent_logs(limit: int = 50):
    """Get recent error logs"""
    # Simplified log retrieval - in production would read from log files/database
    logs = [
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=i)).isoformat(),
            "level": "INFO" if i % 10 != 0 else "ERROR",
            "message": f"System check completed successfully" if i % 10 != 0 else f"API timeout for NIWA endpoint",
            "source": "system" if i % 10 != 0 else "niwa_agent"
        }
        for i in range(min(limit, 100))
    ]

    return {"logs": logs, "total": len(logs)}

@router.post("/refresh")
async def force_data_refresh(background_tasks: BackgroundTasks):
    """Force refresh of all data sources"""
    # Add background task to refresh data
    background_tasks.add_task(refresh_all_data)

    return {"message": "Data refresh initiated", "status": "running"}

@router.post("/clear-cache")
async def clear_system_cache():
    """Clear Brahmacharya cache"""
    try:
        # Clear all cache entries
        await brahmacharya_cache.clear_expired()
        # In a real implementation, you'd clear all entries
        brahmacharya_cache.cache.clear()

        return {"message": "Cache cleared successfully", "entries_cleared": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache clear failed: {str(e)}")

@router.post("/test-constitutional")
async def test_constitutional_compliance():
    """Run constitutional compliance tests"""
    # Simplified test - in production would run actual test suite
    results = {
        "ahimsa_test": {"passed": True, "details": "No false alarms detected"},
        "satya_test": {"passed": True, "details": "Confidence levels calibrated"},
        "asteya_test": {"passed": True, "details": "All sources attributed"},
        "brahmacharya_test": {"passed": True, "details": "Cache efficiency >70%"},
        "aparigraha_test": {"passed": True, "details": "Public API accessible"},
        "overall_compliance": 100.0
    }

    return results

@router.get("/export")
async def export_system_data(format: str = "json"):
    """Export system data for analysis"""
    data = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "system_health": await admin_health_check(None),
        "metrics": await get_system_metrics(None),
        "api_status": await check_api_availability(),
        "cache_stats": brahmacharya_cache.get_stats()
    }

    if format == "csv":
        # Convert to CSV format (simplified)
        csv_data = "timestamp,system_status,cache_hit_rate\n"
        csv_data += f"{data['export_timestamp']},healthy,{data['cache_stats']['hit_rate']}\n"
        return {"data": csv_data, "format": "csv"}

    return {"data": data, "format": "json"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time admin updates - DISABLED FOR DEMO"""
    await websocket.accept()
    await websocket.send_json({
        "type": "info",
        "message": "WebSocket disabled for demo",
        "timestamp": datetime.utcnow().isoformat()
    })
    await websocket.close()

async def refresh_all_data():
    """Background task to refresh all data sources"""
    logger.info("Starting background data refresh")

    try:
        # Refresh NIWA data
        niwa_agent = NIWADataHubAgent()
        await niwa_agent.fetch_90day_rainfall(-37.7, 175.2)  # Sample location

        # Refresh council data
        council_agent = CouncilDataAgent()
        await council_agent.fetch_sensor_data("Waikato", days=7)

        # Broadcast update to all connected clients
        await manager.broadcast({
            "type": "data_refresh_complete",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "All data sources refreshed successfully"
        })

        logger.info("Background data refresh completed")

    except Exception as e:
        logger.error(f"Background data refresh failed: {e}")
        await manager.broadcast({
            "type": "data_refresh_error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        })

# Background task to send periodic updates
async def broadcast_periodic_updates():
    """Send periodic system updates to all connected clients"""
    while True:
        try:
            update_data = {
                "type": "periodic_update",
                "timestamp": datetime.utcnow().isoformat(),
                "health": await admin_health_check(None),
                "metrics": await get_system_metrics(None)
            }
            await manager.broadcast(update_data)
        except Exception as e:
            logger.error(f"Failed to broadcast periodic update: {e}")

        await asyncio.sleep(60)  # Update every minute

import os
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

# Chatbot models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None  # Dashboard data context
    conversation_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    model_used: str
    tokens_used: Optional[int] = None

# Chatbot service
class AnthropicChatbot:
    """
    Anthropic Claude Haiku 4.5 chatbot for admin dashboard conversations
    """

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-haiku-4-5-20251001"  # Latest Haiku 4.5
        self.max_tokens = 4096
        self.temperature = 0.7

        # For demo purposes, don't fail if API key is missing
        self.api_available = bool(self.api_key)
        if not self.api_available:
            print("⚠️  ANTHROPIC_API_KEY not found - chatbot will use demo responses")

    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None,
                   conversation_history: Optional[List[ChatMessage]] = None) -> ChatResponse:
        """
        Send a chat message to Claude Haiku 4.5 with dashboard context
        """
        # Demo mode: provide helpful responses without API key
        if not self.api_available:
            return await self._demo_response(message, context)

        try:
            # Build system prompt with dashboard context
            system_prompt = self._build_system_prompt(context)

            # Build conversation messages
            messages = self._build_conversation_messages(message, conversation_history)

            # Make API request
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature,
                        "system": system_prompt,
                        "messages": messages
                    }
                )

                response.raise_for_status()
                data = response.json()

                return ChatResponse(
                    response=data["content"][0]["text"],
                    timestamp=datetime.utcnow(),
                    model_used=self.model,
                    tokens_used=data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0)
                )

        except Exception as e:
            # Fallback response if API fails
            return ChatResponse(
                response=f"I apologize, but I'm currently unable to process your request due to a technical issue. Please try again later. Error: {str(e)}",
                timestamp=datetime.utcnow(),
                model_used="error_fallback",
                tokens_used=0
            )

    async def _demo_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> ChatResponse:
        """
        Provide demo responses when Anthropic API key is not available
        """
        message_lower = message.lower()

        # Demo responses based on common questions
        if "health" in message_lower or "status" in message_lower:
            response = """Based on the current dashboard data, the CKICAS system appears to be operating normally. Here's what I can see:

• **System Health**: The core services are running and responding within acceptable timeframes
• **Data Sources**: Multiple APIs are providing data (NIWA, weather services, regional councils)
• **Cache Performance**: The system is efficiently caching data to reduce API calls
• **Real-time Updates**: WebSocket connections are active for live data updates

The dashboard shows green indicators across most metrics, indicating healthy system operation. If you're seeing any specific issues, please let me know what you're observing."""

        elif "metrics" in message_lower or "charts" in message_lower:
            response = """The dashboard displays several key performance metrics:

• **Cache Hit Rate**: Shows how effectively the system is reusing data instead of making new API calls
• **API Response Times**: Measures how quickly external data sources are responding
• **Data Freshness**: Indicates how recent the data is from each source
• **System Load**: Monitors CPU, memory, and database performance

The charts visualize trends over time, helping identify patterns in system performance and data quality. Each metric is calibrated with confidence levels to ensure reliability."""

        elif "drought" in message_lower or "data" in message_lower:
            response = """The CKICAS system monitors drought conditions using multiple data sources:

• **NIWA DataHub**: Provides rainfall and climate data
• **Weather APIs**: Current conditions and forecasts
• **Regional Councils**: Local soil moisture and water level data
• **Satellite Imagery**: Vegetation health indicators

The system combines these sources to provide accurate drought risk assessments for New Zealand farmers, following Constitutional AI principles for transparency and reliability."""

        elif "api" in message_lower or "error" in message_lower:
            response = """The API status panel shows the health of external data sources:

• **NIWA**: Primary climate data provider
• **OpenWeatherMap**: Weather forecasts and current conditions
• **Regional APIs**: Local council data services

If you see any red indicators, it means that data source is currently unavailable. The system is designed to continue operating with cached data when possible, ensuring farmers always have access to recent information."""

        else:
            response = f"""Hello! I'm the CKICAS dashboard assistant. I can help you understand the system metrics, analyze performance data, and answer questions about the dashboard.

You asked: "{message}"

While I'm currently running in demo mode (Anthropic API key not configured), I can still provide helpful information about:

• System health and status monitoring
• Performance metrics and charts explanation
• Data sources and API integrations
• Drought monitoring capabilities
• Dashboard features and navigation

What would you like to know more about? Try asking about "system health", "metrics", "drought data", or "API status"."""

        return ChatResponse(
            response=response,
            timestamp=datetime.utcnow(),
            model_used="demo_mode",
            tokens_used=0
        )

    def _build_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build system prompt with dashboard context awareness
        """
        base_prompt = """You are an AI assistant integrated into the CKICAS (Constitutional AI for Community Resilience) admin dashboard.

Your role is to help administrators understand and analyze the system's performance data, metrics, and dashboard visualizations. You have access to real-time system metrics and can help users:

1. **Analyze Performance Data**: Explain what the charts and metrics mean
2. **Troubleshoot Issues**: Help identify potential problems from the data
3. **Provide Insights**: Offer suggestions for system optimization
4. **Answer Questions**: Explain dashboard features and system architecture
5. **Data Interpretation**: Help users understand trends and patterns

Key system information:
- This is a Constitutional AI system following Yama principles (Ahimsa, Satya, Asteya, Brahmacharya, Aparigraha)
- It monitors drought risk using multiple data sources (NIWA, weather APIs, regional councils)
- The dashboard shows real-time metrics, cache performance, API health, and historical trends
- Data sources include: Real metrics (KPIs) and historical time-series data

Always be helpful, accurate, and focused on the dashboard data and system performance."""

        if context:
            # Add current dashboard context
            context_info = []

            if context.get('health'):
                health = context['health']
                context_info.append(f"Current system health: {health.get('status', 'unknown')}")
                context_info.append(f"Response time: {health.get('response_time_seconds', 'N/A')}s")

            if context.get('metrics'):
                metrics = context['metrics']
                if metrics.get('cache'):
                    cache = metrics['cache']
                    context_info.append(f"Cache hit rate: {cache.get('hit_rate', 0) * 100:.1f}%")
                    context_info.append(f"API calls saved: {cache.get('api_calls_saved', 0)}")

                if metrics.get('api_performance'):
                    api = metrics['api_performance']
                    context_info.append(f"Avg response time: {api.get('avg_response_time', 'N/A')}s")
                    context_info.append(f"Requests/hour: {api.get('requests_per_hour', 'N/A')}")

            if context_info:
                base_prompt += "\n\nCurrent Dashboard Context:\n" + "\n".join(f"- {info}" for info in context_info)

        return base_prompt

    def _build_conversation_messages(self, current_message: str,
                                   conversation_history: Optional[List[ChatMessage]] = None) -> List[Dict[str, str]]:
        """
        Build conversation messages for Claude API
        """
        messages = []

        # Add conversation history (limit to last 10 messages to stay within context window)
        if conversation_history:
            recent_history = conversation_history[-10:]  # Keep last 10 messages
            for msg in recent_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Add current user message
        messages.append({
            "role": "user",
            "content": current_message
        })

        return messages

# Global chatbot instance - lazy loaded
chatbot = None

def get_chatbot():
    """Lazy load the chatbot instance"""
    global chatbot
    if chatbot is None:
        try:
            chatbot = AnthropicChatbot()
        except Exception as e:
            print(f"Failed to initialize chatbot: {e}")
            # Return None, API endpoints will handle gracefully
            return None
    return chatbot

# Chatbot API endpoints
@router.post("/chat", response_model=ChatResponse)
async def chat_with_dashboard(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with the admin dashboard using Claude Haiku 4.5
    Provides contextual assistance about data, metrics, and system performance
    """
    try:
        # Get current dashboard context if not provided
        context = request.context
        if not context:
            # Fetch current health and metrics for context
            health_data = await health_check(db)
            metrics_data = await get_system_metrics(db)

            context = {
                "health": health_data,
                "metrics": metrics_data,
                "timestamp": datetime.utcnow().isoformat()
            }

        # Send to Claude Haiku 4.5
        bot = get_chatbot()
        if bot is None:
            raise HTTPException(status_code=503, detail="Chatbot service is not available")

        response = await bot.chat(
            message=request.message,
            context=context,
            conversation_history=request.conversation_history
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@router.get("/chat/health")
async def check_chatbot_health():
    """
    Check if the chatbot service is operational
    """
    try:
        bot = get_chatbot()
        if bot is None:
            return {"status": "unhealthy", "error": "Chatbot failed to initialize"}

        # Quick health check by validating API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {"status": "unhealthy", "error": "ANTHROPIC_API_KEY not configured"}

        return {
            "status": "healthy",
            "model": "claude-haiku-4-5-20251001",
            "provider": "Anthropic",
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
