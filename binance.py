import datetime
from binance_common.configuration import ConfigurationRestAPI
from binance_sdk_spot.spot import Spot

from classes import ApiConfig, StatSchema
from logger import get_logger


logger = get_logger(__name__)


def get_day_stat(api: ApiConfig):
    client = Spot(
        ConfigurationRestAPI(
            api_key=api.key,
            api_secret=api.secret,
        )
    )

    balance_usdt = get_balance(client)
    pnl_value, pnl_percent = get_pnl(client, balance_usdt)

    return StatSchema(
        balance=balance_usdt,
        pnl=pnl_value,
        pnl_percent=pnl_percent,
    )


def get_orders_history(api: ApiConfig, period: datetime.datetime):
    ...