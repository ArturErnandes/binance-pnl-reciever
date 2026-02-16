from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
import html

from config import db_data
from classes import StatHistorySchema, StatPostSchema
from logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    f'postgresql+asyncpg://{db_data.admin}:{db_data.password}@{db_data.host}:{db_data.port}/{db_data.db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_stat_history(bot_id: str):
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
            short_err = html.unescape(str(e))

            logger.exception(f"Ошибка получения истории PnL | bot_id: {bot_id} | error: {short_err}")
            return []


async def post_day_stat(bot_id: str, day_stat: StatPostSchema):
    ...