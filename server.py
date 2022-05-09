import asyncio
import sys
from pathlib import Path
from typing import Any, List, MutableMapping, Optional

import toml
import typer
import uvicorn
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel, EmailStr
from starlette.middleware.cors import CORSMiddleware
from tortoise import run_async
from tortoise.contrib.starlette import register_tortoise

from aerich_config import DATABASE_URL
from api.apiv1.all_routers import api_router

from utils.create_superuser import util_create_superuser
from utils.populate import Populate
from utils import utils
from api import deps

from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware

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

app.add_middleware(PyInstrumentProfilerMiddleware)


class out_non_auth(BaseModel):
    RTI: str = "Tracker"


class out_auth(BaseModel):
    RTI: str = "TrackerAuth"


class dec:
    def __init__(self, auth_schema, non_auth_schema, func):
        breakpoint()
        self.auth_schema = auth_schema
        self.non_auth_schema = non_auth_schema
        self.func = func

    def __call__(self, *args, **kwargs) -> Any:
        # async def wrapper(*args, **kwargs):
        # breakpoint()
        print("yellow")
        return self.func(*args, **kwargs)

        # return wrapper


def make_deco(func):
    async def wrapper(*args, **kwargs):
        print("yellow")
        breakpoint()
        return await func(*args, **kwargs)

    return wrapper


def whichone(response, auth, notauth):
    breakpoint()


# @make_deco
# @dec(out_auth, out_non_auth)
@app.get(
    "/RTIApiv1/hello",
    summary="Test Api Call",
    # response_model=whichone(Response, out_non_auth, out_auth),
    # response_model=out_non_auth
)
async def test_api(request: Request):
    """
    Test API

    :returns: {"RTI": "Tracker"}
    """
    breakpoint()
    return {"RTI": "Tracker"}


app.include_router(api_router, prefix="/apiv1")


@typer_app.command()
def run() -> None:
    if config["debug"]["set"]:
        if __name__ == "__main__":
            serv = uvicorn.Server(
                uvicorn.Config(
                    reload=True,
                    app=app,
                    host=config["debug"]["host"],
                    port=config["debug"]["port"],
                )
            )
            serv.run()
    else:
        uvicorn.run(app)


@typer_app.command()
def populate_user(amount: Optional[int] = 10) -> None:
    async def _run():
        await utils.init_tortoise()
        populator: Populate = await Populate.init()
        await populator.populate_user(amount=amount)

    run_async(_run())


@typer_app.command()
def populate_rti(amount: Optional[int] = 10, response: Optional[bool] = True) -> None:
    async def _run():
        await utils.init_tortoise()
        populator: Populate = await Populate.init()
        await populator.populate_rti(amount=amount, response=response)

    run_async(_run())


@typer_app.command()
def populate_file_upload(amount: Optional[int] = 10) -> None:
    async def _run():
        await utils.init_tortoise()
        populator: Populate = await Populate.init()
        await populator.populate_file_upload(amount=amount)

    run_async(_run())


@typer_app.command()
def populate_topic(topics: Optional[List[str]] = None) -> None:
    async def _run():
        await utils.init_tortoise()
        populator: Populate = await Populate.init()
        await populator.populate_topic(topics)

    run_async(_run())


@typer_app.command()
def populate(
    amount_user: Optional[int] = 100,
    topics_list: Optional[List[str]] = None,
    amount_file_upload: Optional[int] = 500,
    amount_rti: Optional[int] = 500,
    rti_response: Optional[bool] = True,
):
    populate_user(amount=amount_user)
    populate_topic(topics=topics_list)
    populate_file_upload(amount=amount_file_upload)
    populate_rti(amount=amount_rti, response=rti_response)


@typer_app.command()
def create_superuser(
    username: str = typer.Option("", help="Username of the new superuser"),
    email: str = typer.Option("", help="Email of the new superuser"),
    password: str = typer.Option("", help="Password of the new superuser"),
    fullname: str = typer.Option("", help="Fullname of the new superuser"),
) -> None:
    if not username:
        username: str = typer.prompt("Enter superadmin's username")

    if not email:
        email: EmailStr = typer.prompt("Enter superadmin's email", type=EmailStr)

    if not password:
        password: str = typer.prompt(
            "Enter superadmin's password", hide_input=True, confirmation_prompt=True
        )

    if not fullname:
        fullname: str = typer.prompt("Enter superadmin's full name", type=str)

    run_async(
        util_create_superuser(
            username=username, email=email, password=password, full_name=fullname
        )
    )


if __name__ == "__main__":
    typer_app()
