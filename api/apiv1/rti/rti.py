from datetime import datetime
from typing import Any, List, MutableMapping

from pydantic import EmailStr

import api.utils
from api import deps
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from models import Rti
from models.file_upload import FileUpload
from schemas import rti
import toml

router = APIRouter()

config: MutableMapping[str, Any] = toml.load("config.toml")

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

    RtiObj: Rti = await Rti.create(
        **_kwargs
    )

    await RtiObj.save()

    return api.utils.remove_meta_rti(dict(RtiObj))


@router.post("/delete")
async def delete_rti(
    content: rti.RtiDeleteIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    RtiObj = await Rti.get(id=content.id)
    
    if not RtiObj:
        raise HTTPException(status_code=404, detail="Rti not found")
    
    await RtiObj.delete()

    return {"Result": "OK"}

