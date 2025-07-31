from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views.auth import auth_router
from app.views.root import router as root_router
import uvicorn
from config import get_settings

app = FastAPI()
settings = get_settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.middleware.cors.allow_origins,
    allow_credentials=settings.middleware.cors.allow_credentials,
    allow_methods=settings.middleware.cors.allow_methods,
    allow_headers=settings.middleware.cors.allow_headers,
)

app.include_router(auth_router)
app.include_router(root_router)