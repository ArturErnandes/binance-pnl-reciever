from fastapi import FastAPI

from app import app_endpoints
from logger import get_logger


logger = get_logger(__name__)

app = FastAPI()

app.include_router(app_endpoints)
