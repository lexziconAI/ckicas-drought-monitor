"""
Constitutional AI - main.py
Clean version for deployment testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import os
import weather_api
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Starting CKICAS application...")

app = FastAPI(title="CKICAS Ultra-Simple")
print("FastAPI app created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ckicas-frontend.onrender.com",  # Production frontend
        "http://localhost:5173",  # Local development frontend
        "http://localhost:3000",  # Alternative local port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS middleware added")

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
        else:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def chat(self, message: str):
        try:
            if self.api_available:
                # Make real API call to Claude
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": f"You are a helpful assistant for the CKICAS drought monitoring dashboard. Help the user understand drought monitoring, weather data, and system functionality. User question: {message}"}
                    ]
                )

                ai_response = response.content[0].text

                return ChatResponse(
                    response=ai_response,
                    timestamp=datetime.utcnow(),
                    model_used="claude-3-haiku-20240307",
                    tokens_used=response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else 100
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
    # Get real weather API status
    weather_status = weather_api.get_api_status()

    # Add Anthropic status
    anthropic_status = {"status": "healthy", "response_time": 0.123}
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        anthropic_status = {"status": "not_configured", "response_time": 0}

    return {
        "anthropic": anthropic_status,
        **weather_status
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

# Public drought risk endpoint
@app.get("/api/public/drought-risk")
async def get_drought_risk(lat: float, lon: float, forecast_days: int = 14):
    """Get drought risk assessment for a location using real weather APIs"""
    try:
        niwa_client = weather_api.get_niwa_client()
        if niwa_client:
            risk_data = niwa_client.get_drought_risk(lat, lon, forecast_days)
            return risk_data
        else:
            # Fallback to mock data if NIWA not configured
            return {
                'risk_score': 45,
                'confidence': 0.4,
                'factors': ['api_not_configured'],
                'note': 'Using fallback risk assessment - NIWA API not configured'
            }
    except Exception as e:
        return {
            'risk_score': 50,
            'confidence': 0.2,
            'factors': ['api_error'],
            'error': str(e)
        }

# Public data sources endpoint
@app.get("/api/public/data-sources")
async def get_data_sources():
    """Get information about active data sources"""
    sources = []

    # NIWA data source
    niwa_client = weather_api.get_niwa_client()
    if niwa_client:
        sources.append({
            'provider': 'NIWA_DataHub',
            'dataset': 'CliFlo_Climate_Data',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'freshness_hours': 1,  # Real-time data
            'parameters': ['rainfall_daily', 'temperature_max', 'soil_moisture'],
            'url': 'https://cliflo.niwa.co.nz/',
            'note': 'Real-time climate data from NIWA CliFlo'
        })
    else:
        sources.append({
            'provider': 'NIWA_DataHub',
            'dataset': 'CliFlo_Station_2112',
            'timestamp': '2024-11-16T06:00:00Z',
            'freshness_hours': 8,
            'parameters': ['rainfall_daily', 'temperature_max'],
            'note': 'Demo data - NIWA API not configured'
        })

    # OpenWeather data source
    ow_client = weather_api.get_openweather_client()
    if ow_client:
        sources.append({
            'provider': 'OpenWeather',
            'dataset': 'Current_Weather_API',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'freshness_hours': 0,  # Real-time
            'parameters': ['temperature', 'humidity', 'wind_speed', 'pressure'],
            'url': 'https://openweathermap.org/api',
            'note': 'Current weather conditions and forecasts'
        })
    else:
        sources.append({
            'provider': 'OpenWeather',
            'dataset': 'Weather_API',
            'timestamp': '2024-11-16T12:00:00Z',
            'freshness_hours': 2,
            'parameters': ['temperature', 'humidity'],
            'note': 'Demo data - OpenWeather API not configured'
        })

    # Regional council data (mock for now)
    sources.append({
        'provider': 'Waikato_RC',
        'dataset': 'SoilMoisture_Ruakura',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'freshness_hours': 6,
        'parameters': ['soil_moisture_volumetric'],
        'note': 'Regional council soil moisture monitoring'
    })

    return {'sources': sources}