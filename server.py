import sys
from pathlib import Path
from typing import Any, MutableMapping

import toml
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise

from aerich_config import DATABASE_URL
from api.apiv1.all_routers import api_router

path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

app: FastAPI = FastAPI()


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
async def TestApi():
    """
    Test API

    :returns: {"RTI": "Tracker"}
    """
    return {"RTI": "Tracker"}


app.include_router(api_router, prefix="/apiv1")

if config["debug"]["set"]:
    if __name__ == "__main__":
        uvicorn.Config(
            reload=True,
            app=app,
            host=config["debug"]["host"],
            port=config["debug"]["port"],
        )
        uvicorn.run(app, host="0.0.0.0", port=8080)
