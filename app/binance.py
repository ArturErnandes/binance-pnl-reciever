import datetime
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

from classes import ApiConfig, StatSchema
from logger import get_logger


logger = get_logger(__name__)

BASE_URL = "https://api.binance.com"


def get_balance(api: ApiConfig):
    quote_asset = "USDT"
    logger.info("Запрос баланса аккаунта в %s", quote_asset)

    try:
        params = {
            "quoteAsset": quote_asset,
            "timestamp": int(time.time() * 1000),
        }

        query_string = urlencode(params)
        signature = hmac.new(
            api.secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        url = f"{BASE_URL}/sapi/v1/asset/wallet/balance?{query_string}&signature={signature}"
        headers = {"X-MBX-APIKEY": api.key}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        for wallet in data:
            if wallet.get("walletName") == "Spot":
                balance = float(wallet.get("balance", 0) or 0)
                logger.info(f"Баланс успешно получен | {balance} {quote_asset}")
                return balance

        logger.warning("Ошибка получения баланса | Spot wallet не найден")
        raise Exception("spot_wallet_not_found")

    except Exception as e:
        logger.exception(f"Ошибка получения баланса | error: {e}")
        raise Exception(f"get_balance_failed: {e}") from e


def get_orders_history(api: ApiConfig, period: datetime.datetime):
    ...