from typing import Any, List, MutableMapping, Dict, Union

import api.utils
from api.utils import Page, Params
import toml
from api import deps
from fastapi import APIRouter, Depends, HTTPException
from models import Rti
from models.file_upload import FileUpload
from pydantic import UUID4
from schemas import rti
from models.topic import RtiTopic
from fastapi_pagination import paginate
from models import User

router = APIRouter()

config: MutableMapping[str, Any] = toml.load("config.toml")


@router.get("/getall", response_model=Page[rti.RtiOutAuthenticated])
async def get_all_rti(params: Params = Depends()):
    current_user: Union[User, bool] = deps.get_current_active_user_no_raise()

    allRtiObjList = []

    async for RtiObj in Rti.all():
        allRtiObjList.append(await api.utils.ready_rti_obj(RtiObj))

    return paginate(allRtiObjList, params)


@router.get("/get/{id}", response_model=rti.RtiOut)
async def get_rti(id: UUID4) -> Any:
    if not await Rti.exists(id=id):
        raise HTTPException(status_code=404, detail="Rti not found")

    RtiObj: Rti = await Rti.get(id=id)

    return await api.utils.ready_rti_obj(RtiObj)


@router.get("/getResponse/{id}")
async def get_rti_response(id: UUID4) -> Any:
    if not await Rti.exists(id=id):
        raise HTTPException(status_code=404, detail="Rti not found")

    RtiObj: Rti = await Rti.get(id=id)

    await RtiObj.fetch_related("response")

    if not RtiObj.response:
        raise HTTPException(status_code=404, detail="Rti Response not found")

    await RtiObj.response.fetch_related("file")

    return {"response-file": RtiObj.response.file.id, "id": RtiObj.response.id}


@router.post("/add", response_model=rti.RtiOut)
async def create_rti(
    content: rti.RtiIn, current_user=Depends(deps.get_current_active_user)
) -> Any:
    if not await User.exists(id=content.name_of_sender):
        raise HTTPException(status_code=404, detail="Sender user not found!")

    _kwargs = {
        "rti_send_date": content.rti_send_date,
        "title": content.title,
        "registration_number": content.registration_number,
        "email_of_sender": content.email_of_sender,
        "ministry": content.ministry,
        "public_authority": content.public_authority,
        "query": content.query,
        "created_by": current_user,
        "draft": content.draft,
    }

    
    _kwargs["name_of_sender"] = await User.get(id=content.name_of_sender)

    if await FileUpload.exists(id=content.file):
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    RtiObj: Rti = await Rti.create(**_kwargs)

    if content.topic:
        for _topic in content.topic:
            if await RtiTopic.exists(id=_topic):
                topicObj = await RtiTopic.get(id=_topic)
                await RtiObj.topic.add(topicObj)

    await RtiObj.save()

    return RtiObj


@router.put("/update", response_model=rti.RtiOut)
async def update_rti(
    content: rti.RtiUpdateIn, current_user=Depends(deps.get_current_active_user)
) -> Any:
    if not await User.exists(id=content.name_of_sender):
        raise HTTPException(status_code=404, detail="Sender user not found!")

    if not await Rti.exists(id=content.id):
        raise HTTPException(status_code=404, detail="Rti not found")

    RtiObj: Rti = await Rti.get(id=content.id)

    _kwargs = {
        "rti_send_date": content.rti_send_date,
        "registration_number": content.registration_number,
        "title": content.title,
        "name_of_sender": content.name_of_sender,
        "email_of_sender": content.email_of_sender,
        "ministry": content.ministry,
        "public_authority": content.public_authority,
        "query": content.query,
        "created_by": current_user,
        "draft": content.draft,
    }

    _kwargs["name_of_sender"] = await User.get(id=content.name_of_sender)

    FileUploadObjExists = await FileUpload.exists(id=content.file)
    if FileUploadObjExists:
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    await RtiObj.topic.clear()
    if content.topic:
        for _topic in content.topic:
            if await RtiTopic.exists(id=_topic):
                topicObj = await RtiTopic.get(id=_topic)
                await RtiObj.topic.add(topicObj)

    await RtiObj.update_from_dict(_kwargs)

    await RtiObj.save()

    return RtiObj


@router.delete("/delete")
async def delete_rti(
    content: rti.RtiDeleteIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    RtiObj = await Rti.get(id=content.id)

    if not RtiObj:
        raise HTTPException(status_code=404, detail="Rti not found")

    await RtiObj.delete()

    return {}
