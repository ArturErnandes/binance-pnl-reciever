from fastapi import APIRouter

from .config import bots_list
from .classes import BotsListResponse
from .database import get_stat_history_db
from .stat_service import count_day_stat, count_all_balance, make_stat_file
from .logger import get_logger


logger = get_logger(__name__)

app_endpoints = APIRouter()


@app_endpoints.get("/get_bots_list", tags=["Bots"], summary="Получение списка подключенных ботов")
def get_bots_list():
    return BotsListResponse(
        bots={
            bot.key: bot.name
            for bot in bots_list.bots
        }
    )


@app_endpoints.get("/get_day_stat", tags=["PnL"], summary="Получение дневного PnL и баланса")
async def get_day_stat(bot_id: str):
    return await count_day_stat(bot_id)


@app_endpoints.get("/get_stat_history", tags=["PnL"], summary="Получение истории PnL и баланса")
async def get_stat_history(bot_id: str):
    return await get_stat_history_db(bot_id)


@app_endpoints.get("/get_common_balance", tags=["PnL"], summary="Получение текущего баланса всех подключенных ботов")
async def get_common_balance():
    return await count_all_balance()


@app_endpoints.get("/download_stat_history", tags=["PnL"], summary="Загрузка файла со статистикой")
async def download_stat_history(bot_id: str):
    return await make_stat_file(bot_id)


@app_endpoints.get("/get_day_orders", tags=["Orders"], summary="Получение истории ордеров в течении дня")
def get_day_orders(bot_id: str):
    ...


@app_endpoints.get("/get_all_orders", tags=["Orders"], summary="Получение полной истории ордеров")
def get_all_orders(bot_id: str):
    ...