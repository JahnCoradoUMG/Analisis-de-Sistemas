from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="GymFlow API",
    version="1.0.0",
    description="Gym management API with in-memory storage.",
)
app.include_router(api_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
