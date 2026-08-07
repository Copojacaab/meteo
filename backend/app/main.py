from fastapi import FastAPI

app = FastAPI(title="meteo")

@app.get("/api/health")
async def health():
    return {"status": "ok"}