import sys
from pathlib import Path
from typing import Any, MutableMapping

import toml
import typer
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise, run_async
from tortoise.contrib.starlette import register_tortoise

from aerich_config import DATABASE_URL
from api.apiv1.all_routers import api_router
from models.rti import Rti
from models.user import User
from utils import utils

path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

app: FastAPI = FastAPI()
typer_app: typer.Typer = typer.Typer()

config: MutableMapping[str, Any] = toml.load("config.toml")

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
)

# origins = [
#     "..."
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/RTIApiv1/hello", summary="Test Api Call")
async def test_api():
    """
    Test API

    :returns: {"RTI": "Tracker"}
    """
    return {"RTI": "Tracker"}


app.include_router(api_router, prefix="/apiv1")


@typer_app.command()
def run() -> None:
    if config["debug"]["set"]:
        if __name__ == "__main__":
            uvicorn.Config(
                reload=True,
                app=app,
                host=config["debug"]["host"],
                port=config["debug"]["port"],
            )
            uvicorn.run(app)


@typer_app.command()
def create_superuser(
    username: str = typer.Option("", help="Username of the new superuser"),
    email: str = typer.Option("", help="Email of the new superuser"),
    password: str = typer.Option("", help="Password of the new superuser"),
) -> None:
    async def _run():
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={"models": ["models"]},
        )
        userObj = await User.create(
            username=username,
            email=email,
            hashed_password=utils.GetPasswordHash(password),
            is_active=True,
            is_superuser=True,
        )
        await userObj.save()

    run_async(_run())


if __name__ == "__main__":
    typer_app()
