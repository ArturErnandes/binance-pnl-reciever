import datetime

from .classes import StatPostSchema
from .config import bots_list, ApiConfig
from .database import post_day_stat_db, get_yesterday_balance_db
from .binance import get_balance
from .logger import get_logger


logger = get_logger(__name__)


async def post_day_stat():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    logger.info(f"Сохранение статистики | Дата: {today}")

    bots = bots_list.bots

    for bot in bots:
        api = ApiConfig(
            key=bot.api.key,
            secret=bot.api.secret,
        )

        balance = get_balance(api)
        yesterday_balance = await get_yesterday_balance_db(bot.key, yesterday)

        pnl_value = balance - yesterday_balance
        pnl_percent = (pnl_value / 800 * 100)

        day_stat = StatPostSchema(
            bot_id=bot.key,
            date=today,
            balance=balance,
            pnl=pnl_value,
            pnl_percent=pnl_percent,
        )

        await post_day_stat_db(day_stat)