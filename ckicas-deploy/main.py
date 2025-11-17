from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

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

# Root endpoint - serve the frontend
@app.get("/")
async def serve_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CKICAS Drought Monitor</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                text-align: center;
            }
            .header {
                background: rgba(255, 255, 255, 0.1);
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                backdrop-filter: blur(10px);
            }
            h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: 300;
            }
            .status {
                display: inline-block;
                padding: 0.5rem 1rem;
                background: #27ae60;
                color: white;
                border-radius: 20px;
                font-size: 0.9rem;
                margin: 1rem 0;
            }
            .dashboard-placeholder {
                background: rgba(255, 255, 255, 0.1);
                padding: 3rem;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            .loading {
                font-size: 1.2rem;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CKICAS Drought Monitoring Dashboard</h1>
                <div class="status">✅ Backend Connected</div>
            </div>
            <div class="dashboard-placeholder">
                <div class="loading">Loading interactive dashboard...</div>
                <p>Real-time drought monitoring and analysis tools will appear here.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
