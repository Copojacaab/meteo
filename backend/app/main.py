from fastapi import FastAPI

from app.routers.auth import router as auth_router

app = FastAPI(title="meteo")
app.include_router(auth_router)

@app.get("/api/health")
async def health():
    return {"status": "ok"}