from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
    admin: str
    password: str
    host: str
    port: int
    name: str


@dataclass(frozen=True)
class ApiConfig:
    key: str
    secret: str


@dataclass(frozen=True)
class FastApiConfig:
    host: str
    port: int