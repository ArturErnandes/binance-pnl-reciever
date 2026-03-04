import datetime
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from decimal import Decimal

from .classes import ApiConfig
from .logger import get_logger


logger = get_logger(__name__)

BASE_URL = "https://api.binance.com"


def get_balance(api: ApiConfig, ticker: str):
    quote_asset = "USDT"
    headers = {"X-MBX-APIKEY": api.key}

    try:
        base_asset = ticker

        logger.info("Запрос баланса аккаунта | assets=%s + %s", base_asset, quote_asset)

        params = {
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        }
        query_string = urlencode(params)
        signature = hmac.new(api.secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

        account_url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
        account_response = requests.get(account_url, headers=headers, timeout=10)
        account_response.raise_for_status()
        account_data = account_response.json()

        balances = account_data.get("balances", [])
        usdt_amount = Decimal("0")
        ticker_amount = Decimal("0")

        for asset_balance in balances:
            asset = (asset_balance.get("asset") or "").upper()
            free = Decimal(str(asset_balance.get("free", "0")))
            locked = Decimal(str(asset_balance.get("locked", "0")))
            total = free + locked

            if asset == quote_asset:
                usdt_amount = total
            elif asset == base_asset:
                ticker_amount = total

        symbol = f"{base_asset}{quote_asset}"
        price_response = requests.get(
            f"{BASE_URL}/api/v3/ticker/price",
            params={"symbol": symbol},
            timeout=10,
        )
        price_response.raise_for_status()
        price_data = price_response.json()

        if not isinstance(price_data, dict) or "price" not in price_data:
            raise Exception(f"ticker_price_not_found symbol={symbol}")

        price = Decimal(str(price_data["price"]))
        total_balance = usdt_amount + (ticker_amount * price)

        logger.info(
            "Баланс успешно получен | %s %s | ticker=%s amount=%s price=%s",
            float(total_balance),
            quote_asset,
            base_asset,
            str(ticker_amount),
            str(price),
        )
        return float(total_balance)

    except Exception as e:
        logger.exception("Ошибка получения баланса | error: %s", e)
        raise Exception(f"get_balance_failed: {e}") from e


def get_orders_history(api: ApiConfig, period: datetime.datetime):
    ...
