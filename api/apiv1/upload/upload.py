import os
import shutil
from distutils.command.upload import upload
from typing import Any, MutableMapping
from uuid import uuid4

import toml
from api import deps
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from models.file_upload import FileUpload

router = APIRouter()
config: MutableMapping[str, Any] = toml.load("config.toml")


@router.post("/upload/")
async def upload_file(
    uploaded_file: UploadFile = File(...),
    current_user=Depends(deps.get_current_active_user),
) -> str:
    if uploaded_file is not None:
        if uploaded_file.content_type != "application/pdf":
            return HTTPException(422, detail="Only PDF uploads are allowed!")

        path = os.path.join(
            config["settings"]["upload_dir"] + (filename := str(uuid4()) + ".pdf")
        )

        with open(path, "wb") as out_file:
            shutil.copyfileobj(uploaded_file.file, out_file)

        FileUploadObj = await FileUpload.create(
            path=path, filename=filename, created_by=current_user
        )

        await FileUploadObj.save()

        return {"upload_time": FileUploadObj.created_on, "upload_id": FileUploadObj.id}


@router.get("/upload/{id}")
async def upload_file(id: str):
    FileUploadObjExists = await FileUpload.exists(id=id)
    if not FileUploadObjExists:
        return HTTPException(404, detail="Uploaded file not found!")

    FileUploadObj = await FileUpload.get(id=id)
    return {"url": FileUploadObj.path}
