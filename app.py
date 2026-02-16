from fastapi import APIRouter

from logger import get_logger


logger = get_logger(__name__)

app_endpoints = APIRouter()


@app_endpoints.get("/get_day_stat", tags=["PnL"], summary="Получение дневного PnL и баланса")
def get_day_stat(bot_id: str):
    ...


@app_endpoints.post("/get_stat_history", tags=["PnL"], summary="Получение истории PnL и баланса")
async def get_stat_history(bot_id: str):
    ...


@app_endpoints.post("/get_day_orders", tags=["Orders"], summary="Получение истории ордеров в течении дня")
def get_day_orders(bot_id: str):
    ...


@app_endpoints.post("/get_all_orders", tags=["Orders"], summary="Получение полной истории ордеров")
def get_all_orders(bot_id: str):
    ...