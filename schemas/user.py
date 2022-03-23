from pydantic import BaseModel, validator
from pydantic import EmailStr


class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str

    @validator("username")
    def username_check(cls, value):
        assert "@" not in value, 'Please don\'t use "@" in username'
        assert value != "", "Username is empty."
        assert 0 < len(value) <= 15, "Username length greater than 15."
        return value

    @validator("password")
    def check_password_not_empty(cls, v):
        assert v != "", "Password is empty."
        return v

    @validator("email")
    def check_email_not_empty(cls, v):
        assert v != "", "E-Mail is empty."
        return v
