from datetime import datetime
from typing import Any, List, MutableMapping

from pydantic import EmailStr

import api.utils
from api import deps
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from models import Rti, Response
from models.file_upload import FileUpload
from schemas import response
import toml

router = APIRouter()

config: MutableMapping[str, Any] = toml.load("config.toml")

@router.post("/add")
async def create_response(
    content: response.ResponseIn, current_user=Depends(deps.get_current_active_user)
) -> Any:
    _response_recv_date = datetime.fromtimestamp(int(content.response_recv_date))
    
    _kwargs = {
        "response_recv_date": _response_recv_date,
        "created_by": current_user
    }

    RtiObjExists = await Rti.exists(id=content.response_to_rti)
    if not RtiObjExists:
        return HTTPException(404, detail="RTI not found!")
    
    RtiObj = await Rti.get(id=content.response_to_rti)

    if RtiObj.response:
        return HTTPException(404, detail="RTI already has a response!")

    FileUploadObjExists = await FileUpload.exists(id=content.file)
    if FileUploadObjExists:
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    ResponseObj: Response = await Response.create(
        **_kwargs
    )

    await ResponseObj.save()

    RtiObj.response = ResponseObj
    await RtiObj.save()

    return api.utils.remove_meta_rti(dict(ResponseObj))


@router.post("/delete")
async def delete_response(
    content: response.ResponseDeleteIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    ResponseObj = await Response.get(id=content.id)
    
    if not ResponseObj:
        raise HTTPException(status_code=404, detail="Response not found!")
    
    RtiObj: Rti = await Rti.filter(response = ResponseObj)[0]
    await ResponseObj.delete()

    RtiObj.response = None
    await RtiObj.save()

    return {"Result": "OK"}

