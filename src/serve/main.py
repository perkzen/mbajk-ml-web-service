from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .routers import health_router, bike_stations_router, prediction_router

app = FastAPI()

app.include_router(health_router)
app.include_router(bike_stations_router)
app.include_router(prediction_router)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
