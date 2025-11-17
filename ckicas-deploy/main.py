from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="CKICAS Ultra-Simple")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for React assets
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# Basic health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-simple CKICAS running"}

# Serve React app
@app.get("/")
async def serve_react_app():
    return FileResponse("frontend/dist/index.html", media_type="text/html")

# Catch-all route for React Router (SPA routing)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Check if it's a static asset request
    if full_path.startswith("assets/"):
        asset_path = f"frontend/dist/{full_path}"
        if os.path.exists(asset_path):
            return FileResponse(asset_path)
    
    # For all other routes, serve the React app (SPA routing)
    return FileResponse("frontend/dist/index.html", media_type="text/html")
