from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from .config import db_data
from .classes import StatHistorySchema, StatPostSchema
from .logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{db_data.admin}:{db_data.password}@{db_data.host}:{db_data.port}/{db_data.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_stat_history_db(bot_id: str):
    logger.info(f"Запрос истории PnL | Bot_id: {bot_id}")

    query = text("""
                 SELECT day, pnl_value, pnl_percent, balance
                 FROM stats
                 WHERE bot_id = :bot_id
                 ORDER BY day ASC
                 """)

    async with new_session() as session:
        try:
            result = await session.execute(query, {"bot_id": bot_id})
            rows = result.fetchall()

            stat_history: list[StatHistorySchema] = []

            for row in rows:
                pnl_value = float(row.pnl_value)
                pnl_percent_val = float(row.pnl_percent)
                balance = float(row.balance)

                stat_history.append(
                    StatHistorySchema(
                        date=row.day,
                        pnl=pnl_value,
                        pnl_percent=pnl_percent_val,
                        balance=balance
                    ))

            logger.info(f"История PnL успешно получена | Bot_id: {bot_id}")
            return stat_history

        except Exception as e:
            logger.exception(f"Ошибка получения истории PnL | bot_id: {bot_id} | error: {str(e)}")
            return []


async def get_yesterday_balance_db(bot_id, day):
    logger.info("Запрос баланса за предыдущий день")

    query = text("""
                 SELECT balance
                 FROM stats
                 WHERE day = :day AND bot_id = :bot_id
                 """)

    async with new_session() as session:
        try:
            result = await session.execute(query, {"day": day, "bot_id": bot_id})
            balance = float(result.scalar_one_or_none())

            logger.info(f"Баланс успешно получен | {balance}")
            return balance

        except Exception as e:
            logger.exception(f"Ошибка получения баланса | bot_id: {bot_id} day: {day} error: {e}")
            raise RuntimeError(f"balance_not_found bot_id: {bot_id} day: {day}") from e


async def post_day_stat(bot_id: str, day_stat: StatPostSchema):
    ...