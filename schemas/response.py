from typing import Dict, Union
from pydantic import BaseModel, UUID4


class ResponseIn(BaseModel):
    file: UUID4
    response_recv_date: int
    response_to_rti: UUID4

class ResponseOut(BaseModel):
    id: int
    response_recv_date: int
    file: Dict[str, Union[str, UUID4]] = {}

class ResponseUpdateIn(ResponseIn):
    id: UUID4


class ResponseDeleteIn(BaseModel):
    id: UUID4
