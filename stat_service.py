from binance import get_balance
import datetime

from classes import ApiConfig, StatSchema
from database import get_balance
from config import bots_list
from logger import get_logger


logger = get_logger(__name__)


async def get_day_stat(bot_id: str):
    bot = next(b for b in bots_list.bots if b.key == bot_id)

    api = ApiConfig(
        key=bot.api.key,
        secret=bot.api.secret,
    )

    balance = await get_balance(api)
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d/%m/%Y")

    yesterday_balance = get_balance(bot_id, yesterday)

    pnl_value = balance - yesterday_balance
    pnl_percent = (pnl_value / yesterday_balance * 100)

    return StatSchema(
        balance=balance,
        pnl=pnl_value,
        pnl_percent=pnl_percent,
    )