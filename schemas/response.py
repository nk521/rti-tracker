from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, EmailStr


class ResponseIn(BaseModel):
    file: str
    response_recv_date: str
    response_to_rti: str


class ResponseDeleteIn(BaseModel):
    id: str
