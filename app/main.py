from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views.auth import auth_router
from app.views.root import router as root_router
from app.views.loan_management import loan_router
from app.config import get_settings

app = FastAPI()
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(auth_router)
app.include_router(root_router)
app.include_router(loan_router)