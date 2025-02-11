from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.routers.api_router import api_router
from app.settings import settings
tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "CV Analyzer",
        "description": "API that uploads CV and provides a concise summary and improvement of the CV contents.",

    }
]
app = FastAPI(title=settings.PROJECT_NAME, version=__version__,openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
