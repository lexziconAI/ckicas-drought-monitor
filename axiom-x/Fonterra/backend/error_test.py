import sys
import traceback
from fastapi import FastAPI
import uvicorn

try:
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Error test working!"}
    
    @app.on_event("startup")
    async def startup():
        print("STARTUP: Application starting...")
        try:
            # Test imports that might fail
            print("STARTUP: Testing imports...")
            import asyncio
            print("STARTUP: asyncio OK")
            import sqlalchemy
            print("STARTUP: sqlalchemy OK")
            print("STARTUP: All imports successful")
        except Exception as e:
            print(f"STARTUP ERROR: {e}")
            traceback.print_exc()
            sys.exit(1)
    
    @app.on_event("shutdown") 
    async def shutdown():
        print("SHUTDOWN: Application shutting down...")
    
    print("MAIN: Starting uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="debug")
    
except Exception as e:
    print(f"MAIN ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
