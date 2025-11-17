from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Basic uvicorn test working!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
