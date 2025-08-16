from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views.routers import (
    root_router,
    auth_router,
    loan_router,
    record_router,
    utils_router,
)
from app.core.config import get_settings
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger("uvicorn.error")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App is heating up!")
    yield
    logger.info("App shutting down.")


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
app.include_router(utils_router)
