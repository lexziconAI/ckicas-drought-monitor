from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import traceback

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" Starting Ultra-Minimal CKICAS Backend...")
    try:
        yield
    except Exception as e:
        print(f" Error: {e}")
        traceback.print_exc()
    finally:
        print(" Shutting down...")

app = FastAPI(
    title="CKICAS Ultra-Minimal",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include simplified admin routes
from app.api.simple_admin_routes import router as admin_router
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-minimal CKICAS running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
