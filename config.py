import json

from classes import DbConfig, FastApiConfig, TradeBotSchema, BotsList, ApiConfig


data_file = "stat-data.json"

with open(data_file, "r", encoding="utf-8") as f:
    config_data = json.load(f)

db_data = DbConfig(
    admin=config_data["database"]["admin"],
    password=config_data["database"]["password"],
    host=config_data["database"]["host"],
    port=int(config_data["database"]["port"]),
    db_name=config_data["database"]["db_name"],
)

fastapi_data = FastApiConfig(
    host=config_data["app"]["host"],
    port=int(config_data["app"]["port"]),
)

bots_list = BotsList(
    bots=[
        TradeBotSchema(
            key=bot_id,
            name=bot_cfg["name"],
            api=ApiConfig(
                key=bot_cfg["api"]["key"],
                secret=bot_cfg["api"]["secret"],
            ),
        )
        for bot_id, bot_cfg in config_data.get("bots", {}).items()
    ]
)