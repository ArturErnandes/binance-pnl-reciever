import datetime

from .classes import ApiConfig, StatSchema
from .binance import get_balance
from .database import get_yesterday_balance_db
from .config import bots_list
from .logger import get_logger


logger = get_logger(__name__)


async def count_day_stat(bot_id: str):
    bot = next(b for b in bots_list.bots if b.key == bot_id)

    api = ApiConfig(
        key=bot.api.key,
        secret=bot.api.secret,
    )

    balance = get_balance(api)
    yesterday = datetime.date.today() - datetime.timedelta(days=2)

    yesterday_balance = await get_yesterday_balance_db(bot_id, yesterday)

    pnl_value = balance - yesterday_balance
    pnl_percent = (pnl_value / 800 * 100)

    return StatSchema(
        balance=balance,
        pnl=pnl_value,
        pnl_percent=pnl_percent,
    )


async def count_all_balance():
    yesterday = datetime.date.today() - datetime.timedelta(days=2)

    total_balance = 0
    total_yesterday_balance = 0

    bots = bots_list.bots

    for bot in bots:
        api = ApiConfig(
            key=bot.api.key,
            secret=bot.api.secret,
        )

        balance = get_balance(api)
        total_balance += float(balance)

        yesterday_balance = await get_yesterday_balance_db(bot.key, yesterday)

        total_yesterday_balance += float(yesterday_balance)

    pnl_value = total_balance - total_yesterday_balance

    base = 800 * len(bots)
    pnl_percent = (pnl_value / base * 100)

    return StatSchema(
        balance=float(total_balance),
        pnl=float(pnl_value),
        pnl_percent=float(pnl_percent),
    )
