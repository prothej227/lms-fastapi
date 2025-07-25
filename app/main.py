from fastapi import FastAPI
from app.views.auth import auth_router
from app.views.root import router as root_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(root_router)