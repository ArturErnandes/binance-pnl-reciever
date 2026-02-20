from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.app import app_endpoints
from app.config import fastapi_data
from app.logger import get_logger


logger = get_logger(__name__)

app = FastAPI()

app.include_router(app_endpoints)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    logger.info(f"Запуск fastapi | host: {fastapi_data.host} port: {fastapi_data.port}")

    uvicorn.run("main:app", host=fastapi_data.host, port=fastapi_data.port)