from datetime import datetime
from typing import Any, List, MutableMapping

import api.utils
import toml
from api import deps
from fastapi import APIRouter, Depends, HTTPException
from models import Response, Rti
from models.file_upload import FileUpload
from schemas import response

router = APIRouter()

config: MutableMapping[str, Any] = toml.load("config.toml")


@router.post("/add", response_model=response.ResponseOut)
async def create_response(
    content: response.ResponseIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    _kwargs = {
        "response_recv_date": content.response_recv_date,
        "created_by": current_user,
    }

    RtiObjExists = await Rti.exists(id=content.response_to_rti)
    if not RtiObjExists:
        raise HTTPException(404, detail="RTI not found!")

    RtiObj = await Rti.get(id=content.response_to_rti)

    if RtiObj.response:
        raise HTTPException(404, detail="RTI already has a response!")

    breakpoint()
    FileUploadObjExists = await FileUpload.exists(id=content.file)
    if FileUploadObjExists:
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    ResponseObj: Response = await Response.create(**_kwargs)

    await ResponseObj.save()

    RtiObj.response = ResponseObj
    await RtiObj.save()

    ResponseObjDict = dict(ResponseObj)
    ResponseObjDict["file"] = {
        "file": {
            "id": ResponseObj.file.id,
            "filename": ResponseObj.file.filename,
        }
    }
    print(ResponseObjDict)
    return ResponseObjDict


@router.put("/update", response_model=response.ResponseOut)
async def update_response(
    content: response.ResponseUpdateIn,
    current_user=Depends(deps.get_current_active_user),
) -> Any:

    if not await Response.exists(id=content.id):
        raise HTTPException(status_code=404, detail="Rti Response not found")

    ResponseObj: Response = await Response.get(id=content.id)

    RtiObjExists = await Rti.exists(id=content.response_to_rti)
    if not RtiObjExists:
        return HTTPException(404, detail="RTI not found!")

    RtiObj = await Rti.get(id=content.response_to_rti)

    _response_recv_date = datetime.fromtimestamp(int(content.response_recv_date))
    _kwargs = {"response_recv_date": _response_recv_date, "created_by": current_user}

    FileUploadObjExists = await FileUpload.exists(id=content.file)
    if FileUploadObjExists:
        FileUploadObj = await FileUpload.get(id=content.file)
        _kwargs["file"] = FileUploadObj

    await ResponseObj.update_from_dict(_kwargs)
    await ResponseObj.save()

    RtiObj.response = ResponseObj
    await RtiObj.save()

    return ResponseObj


@router.delete("/delete")
async def delete_response(
    content: response.ResponseDeleteIn,
    current_user=Depends(deps.get_current_active_user),
) -> Any:

    ResponseObj = await Response.get(id=content.id)

    if not ResponseObj:
        raise HTTPException(status_code=404, detail="Response not found!")

    RtiObj: Rti = await Rti.filter(response=ResponseObj)[0]
    await ResponseObj.delete()

    RtiObj.response = None
    await RtiObj.save()

    return {}
