from multiprocessing import Process
import uvicorn
import asyncio

from app.app import app
from app.config import fastapi_data
from app.stat_writer import stat_writer
from app.logger import get_logger


logger = get_logger(__name__)


def app_run():
    logger.info(f"Запуск fastapi | host: {fastapi_data.host} port: {fastapi_data.port}")
    uvicorn.run(app, host=fastapi_data.host, port=fastapi_data.port)


def writer_run():
    logger.info("Запуск stat-writer")
    asyncio.run(stat_writer())


if __name__ == "__main__":
    procs = [
        Process(target=writer_run, name="stat-writer"),
        Process(target=app_run, name="fastapi"),
    ]

    for p in procs:
        p.start()

    for p in procs:
        p.join()