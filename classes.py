import datetime
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class DbConfig:
    admin: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass(frozen=True)
class ApiConfig:
    key: str
    secret: str


@dataclass(frozen=True)
class TradeBotSchema:
    key: str
    name: str
    api: ApiConfig


@dataclass(frozen=True)
class BotsList:
    bots: list[TradeBotSchema]


class BotsListResponse(BaseModel):
    bots: dict


@dataclass(frozen=True)
class FastApiConfig:
    host: str
    port: int


@dataclass(frozen=True)
class StatSchema:
    date: datetime.date
    bot_id: str
    pnl: float
    pnl_percent: float