from asyncio import run as async_run
from typing import Any, Dict, Generic, List, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractParams
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.default import Params as BaseParams
from models.rti import Rti

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(10, ge=1, le=1000)


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> BasePage[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        # for item in range(len(items)):
        #     rtiObj: Rti = items[item]
        #     async_run(rtiObj.fetch_related("file"))
        #     async_run(rtiObj.fetch_related("topic"))

        #     if rtiObj.file:
        #         rtiObj.file_id = rtiObj.file.id

        #     if rtiObj.topic:
        #         rtiObj.topics = list()
        #         for temp in rtiObj.topic.all():
        #             rtiObj.topics.append(
        #                 {"id": temp.id,"topic_word": temp.topic_word, "topic_slug": temp.topic_slug}
        #             )

        return cls(
            total=total,
            items=items,
            page=params.page,
            size=params.size,
        )


async def ready_rti_obj(RtiObj: Rti) -> Dict[str, Any]:
    # breakpoint()
    await RtiObj.fetch_related("file")
    await RtiObj.fetch_related("response")
    await RtiObj.fetch_related("topic")
    RtiObjDict = dict(RtiObj)

    if RtiObj.file:
        RtiObjDict["file"] = {"id": RtiObj.file.id, "filename": RtiObj.file.filename}

    if RtiObj.response:
        await RtiObj.response.fetch_related("file")
        RtiObjDict["response"] = {
            "id": RtiObj.response.id,
            "response_recv_date": RtiObj.response.response_recv_date,
            "file": {
                "id": RtiObj.response.file.id,
                "filename": RtiObj.response.file.filename,
            }
        }

    RtiObjDict["topics"] = list(dict())

    async for temp in RtiObj.topic:
        RtiObjDict["topics"].append(
            {
                "id": temp.id,
                "topic_word": temp.topic_word,
                "topic_slug": temp.topic_slug,
            }
        )

    return RtiObjDict


def remove_meta_rti(obj: Dict[str, Any], fields: List[str] = None):
    if fields == None:
        fields = []

    pop_list = ["updated_on", "created_on"]
    pop_list.extend(fields)

    for _pop in pop_list:
        obj.pop(_pop)

    return obj
