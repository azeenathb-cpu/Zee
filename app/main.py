from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Routes
app.include_router(router)


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }