from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import UUID4, BaseModel, EmailStr


class RtiIn(BaseModel):
    rti_send_date: int
    title: str
    registration_number: str
    name_of_sender: UUID4
    email_of_sender: EmailStr
    ministry: int
    public_authority: int
    topic: Optional[List[UUID4]]
    query: str
    file: str
    draft: bool


class FileOut(BaseModel):
    id: UUID4
    filename: str


class RtiOut(BaseModel):
    id: UUID4
    rti_send_date: int
    title: str
    registration_number: str
    ministry: int
    public_authority: int
    query: str
    topics: List[Dict[str, Union[str, UUID4]]] = [{}]
    file: Dict[str, Union[str, UUID4]] = {}
    response: Dict[str, Union[UUID4, int, Dict[str, Union[UUID4, str]]]]


class RtiOutAuthenticated(RtiOut):
    name_of_sender: Optional[Dict[str, Union[str, UUID4]]]
    created_by: Optional[Dict[str, Union[str, UUID4]]]
    draft: Optional[bool]


class RtiUpdateIn(RtiIn):
    id: UUID4


class RtiDeleteIn(BaseModel):
    id: UUID4
