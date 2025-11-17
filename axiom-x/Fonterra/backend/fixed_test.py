from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" FIXED: Application starting...")
    try:
        print("FIXED: Testing imports...")
        import asyncio
        print("FIXED: asyncio OK")
        import sqlalchemy
        print("FIXED: sqlalchemy OK")
        print("FIXED: All imports successful")
        yield
    except Exception as e:
        print(f"FIXED ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print(" FIXED: Application shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Fixed server working!", "status": "stable"}

@app.get("/health")
async def health():
    return {"status": "healthy", "server": "fixed"}
