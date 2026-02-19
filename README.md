# binance-pnl-reciever </h1>
Telegram mini-app for obtaining PnL of specified accounts via Binance Api

<details>
<summary><b>Example of filling in the stat-data.json file</b></summary>

```json
{
  "bot": {
    "token": "token",
    "users": [1234, 5678]
  },
  "app": {
    "host": "127.0.0.1",
    "port": 8000
  },
  "database": {
    "admin": "admin",
    "password": "admin",
    "host": "127.0.0.1",
    "port": 5432,
    "db_name": "my_db"
  },
  "bots": {
    "bot_id": {
      "name": "Bot Name",
      "api": {
        "key": "binance api key",
        "secret": "binance secret key"
      }
    }
  }
}
```
</details>
