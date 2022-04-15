from datetime import datetime
from typing import Any, List, MutableMapping

import api.utils
import toml
from api import deps
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from models import Rti
from models.file_upload import FileUpload
from pydantic import EmailStr
from schemas import rti

router = APIRouter()

config: MutableMapping[str, Any] = toml.load("config.toml")


@router.get("/get/{id}")
async def get_rti(id: str) -> Any:
    if not await Rti.exists(id=id):
        raise HTTPException(status_code=404, detail="Rti not found")

    RtiObj: Rti = await Rti.get(id=id)
    return api.utils.remove_meta_rti(dict(RtiObj))


@router.post("/add")
async def create_rti(
    content: rti.RtiIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    _rti_send_date = datetime.fromtimestamp(int(content.rti_send_date))

    _kwargs = {
        "rti_send_date": _rti_send_date,
        "registration_number": content.registration_number,
        "name_of_sender": content.name_of_sender,
        "email_of_sender": content.email_of_sender,
        "ministry": content.ministry,
        "public_authority": content.public_authority,
        "query": content.query,
        "created_by": current_user,
        # topic=content.topic
    }

    FileUploadObjExists = await FileUpload.exists(id=content.file)
    if FileUploadObjExists:
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    RtiObj: Rti = await Rti.create(**_kwargs)

    await RtiObj.save()

    return api.utils.remove_meta_rti(dict(RtiObj))


@router.put("/update")
async def update_rti(
    content: rti.RtiUpdateIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    if not await Rti.exists(id=content.id):
        raise HTTPException(status_code=404, detail="Rti not found")

    RtiObj: Rti = await Rti.get(id=content.id)

    _rti_send_date = datetime.fromtimestamp(int(content.rti_send_date))

    _kwargs = {
        "rti_send_date": _rti_send_date,
        "registration_number": content.registration_number,
        "name_of_sender": content.name_of_sender,
        "email_of_sender": content.email_of_sender,
        "ministry": content.ministry,
        "public_authority": content.public_authority,
        "query": content.query,
        "created_by": current_user,
        # topic=content.topic
    }

    FileUploadObjExists = await FileUpload.exists(id=content.file)
    if FileUploadObjExists:
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    await RtiObj.update_from_dict(_kwargs)

    await RtiObj.save()

    return api.utils.remove_meta_rti(dict(RtiObj))


@router.delete("/delete")
async def delete_rti(
    content: rti.RtiDeleteIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    RtiObj = await Rti.get(id=content.id)

    if not RtiObj:
        raise HTTPException(status_code=404, detail="Rti not found")

    await RtiObj.delete()

    return {"Result": "OK"}
