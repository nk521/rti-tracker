from typing import List
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

class RtiDeleteIn(BaseModel):
    id: str
