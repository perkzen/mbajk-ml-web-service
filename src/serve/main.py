from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from .routers import health_router, bike_stations_router, prediction_router
from ..models.model_registry import download_model_registry

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(bike_stations_router)
app.include_router(prediction_router)


@app.on_event("startup")
async def startup_event():
    download_model_registry()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
