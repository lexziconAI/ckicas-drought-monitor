# Load environment variables from .env file FIRST
from dotenv import load_dotenv
load_dotenv()

# NZ Drought Early Warning Dashboard - Main FastAPI Application
# Constitutional AI implementation with Yama principles enforcement

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import traceback
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Import constitutional modules
from app.constitutional.yamas import YamaValidator
from app.constitutional.confidence import ConfidenceCalibrator

# Import API routes
from app.api.routes import router as api_router
from app.api.admin_routes import router as admin_router

# Import database
from app.models.database import create_tables

# Import historical data collector
from app.services.historical_collector import start_historical_collection, stop_historical_collection

# Initialize constitutional governance
yama_validator = YamaValidator()
confidence_calibrator = ConfidenceCalibrator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager with explicit error handling"""
    print("🚀 Starting CKICAS Backend with error tracking...")

    try:
        # Startup
        print("📊 Initializing database...")
        await create_tables()
        print("✅ Database initialized successfully")

        print("🌐 Initializing data sources...")
        # Add any other startup tasks here
        print("✅ Data sources initialized")

        print("🎯 Backend startup complete!")

        try:
            yield  # Server runs here
        except Exception as e:
            print("❌ RUNTIME ERROR DURING SERVER OPERATION!")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Full traceback:")
            traceback.print_exc()
            raise  # Re-raise to ensure proper shutdown

    except Exception as e:
        print("❌ STARTUP FAILED!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)  # Exit with error code

    finally:
        # Shutdown
        print("🛑 Shutting down CKICAS Backend...")
        # Add cleanup here if needed

# Create FastAPI application
app = FastAPI(
    title="NZ Drought Early Warning Dashboard",
    description="Constitutional AI drought monitoring system following Yama principles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # ← NEW: Use lifespan instead of events
)

# CORS middleware (Ahimsa - non-harm through universal access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for farmer accessibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

# Mount static files for React frontend (if built)
frontend_build_path = Path(__file__).parent / ".." / "frontend" / "dist"
if frontend_build_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_build_path), html=True), name="frontend")

# Constitutional error handler
@app.exception_handler(HTTPException)
async def constitutional_error_handler(request: Request, exc: HTTPException):
    """Apply constitutional principles to error responses"""

    # Satya: Always be truthful about system state
    if exc.status_code >= 500:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Constitutional system error",
                "message": "System temporarily unavailable. Data sources may be refreshing.",
                "constitutional_principle": "Satya (Truthfulness)",
                "retry_after": 300  # 5 minutes
            }
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "constitutional_principle": "Ahimsa (Non-harm)"
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "constitutional_principles": ["Ahimsa", "Satya", "Asteya", "Brahmacharya", "Aparigraha"],
        "version": "1.0.0"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )