from typing import Any, MutableMapping

import toml

config: MutableMapping[str, Any] = toml.load("config.toml")

if (db := config["settings"]["db"]) == "sqlite":
    DATABASE_URL = f"sqlite://{config['sqlite']['dbfile']}"
elif db == "postgres":
    DATABASE_URL = f"postgres://{config['postgres']['username']}:{config['postgres']['password']}@{config['postgres']['server']}:{config['postgres']['port']}/{config['postgres']['db_name']}"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
