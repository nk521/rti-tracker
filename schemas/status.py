from pydantic import BaseModel
from pydantic import EmailStr


class StatusIn(BaseModel):
    registeration: str
    email: EmailStr
