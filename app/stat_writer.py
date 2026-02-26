import datetime
import asyncio

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


async def stat_writer():
    while True:
        now = datetime.datetime.now()

        run_at = now.replace(hour=23, minute=59, second=0, microsecond=0)
        if run_at <= now:
            run_at += datetime.timedelta(days=1)

        sleep_sec = int((run_at - now).total_seconds())

        h = sleep_sec // 3600
        m = (sleep_sec % 3600) // 60
        s = sleep_sec % 60

        logger.info(
            f"Запись статистики | следующий запуск: {run_at:%Y-%m-%d %H:%M:%S} | sleep={h:02d}:{m:02d}:{s:02d}"
        )

        await asyncio.sleep(sleep_sec)

        try:
            await post_day_stat()
        except Exception:
            logger.exception("Планировщик статистики | ошибка при post_day_stat")