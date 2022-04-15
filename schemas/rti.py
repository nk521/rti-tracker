from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, EmailStr


class RtiIn(BaseModel):
    rti_send_date: str
    registration_number: str
    name_of_sender: str
    email_of_sender: EmailStr
    ministry: int
    public_authority: int
    topic: List[str]
    query: str
    file: str


class RtiUpdateIn(BaseModel):
    id: str
    rti_send_date: str
    registration_number: str
    name_of_sender: str
    email_of_sender: EmailStr
    ministry: int
    public_authority: int
    topic: List[str]
    query: str
    file: str


class RtiDeleteIn(BaseModel):
    id: str
