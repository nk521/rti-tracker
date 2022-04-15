from pydantic import BaseModel, EmailStr


class StatusIn(BaseModel):
    registeration: str
    email: EmailStr
