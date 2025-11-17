from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import traceback

# Import API routes
from app.api.routes import router as api_router
from app.api.admin_routes import router as admin_router

# Import database
from app.models.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" Starting Minimal CKICAS Backend...")
    try:
        print(" Initializing database...")
        await create_tables()
        print(" Database ready")
        yield
    except Exception as e:
        print(f" Error: {e}")
        traceback.print_exc()
    finally:
        print(" Shutting down...")

app = FastAPI(
    title="CKICAS Minimal",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Minimal CKICAS running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
