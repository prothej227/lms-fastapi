from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views.auth import auth_router
from app.views.root import router as root_router
from app.views.loan_management import loan_router
from app.views.records import record_router
from app.core.config import get_settings
from app.core import state
from app.utils.static_data import load_reference_mappings_config
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger("uvicorn.error")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.ReferenceValueMappings = load_reference_mappings_config()
    logger.info("Reference value mappings loaded on startup.")
    yield
    logger.info("App shutting down...")


app = FastAPI(lifespan=lifespan)

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
app.include_router(record_router)
