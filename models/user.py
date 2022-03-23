from pydantic import EmailStr
from schemas import user
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from models.utils import extra_fields


class User(models.Model):
    """
    User Model Class
    - Base class with basic functionality
    """

    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=15, unique=True, null=False)
    email: EmailStr = extra_fields.EmailField(index=True, unique=True, null=False)
    hashed_password = fields.CharField(default="", max_length=500, null=False)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    created_on = fields.DatetimeField(auto_now_add=True)
    updated_on = fields.DatetimeField(auto_now=True)
    deleted = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = [
            "hashed_password",
            "is_active",
            "is_superuser",
            "create_on",
            "updated_on",
        ]


UserPydantic = pydantic_model_creator(User, name="User", exclude=["created_on"])
UserPydanticList = pydantic_queryset_creator(User)
UserInPydantic = user.UserIn
