from pydantic import EmailStr, UUID4
from models.topic import RtiTopic
from tortoise import fields, models
from datetime import datetime

from models.utils import extra_fields
from models.user import User
from models.response import Response


class Rti(models.Model):
    id: UUID4 = fields.UUIDField(pk=True)
    created_on: datetime = fields.DatetimeField(auto_now_add=True)
    updated_on: datetime = fields.DatetimeField(auto_now=True)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="creator_rti"
    )
    rti_send_date: datetime = fields.DatetimeField()
    registration_number: str = fields.CharField(max_length=50, unique=True)
    name_of_sender: str = fields.CharField(max_length=50)
    email_of_sender: EmailStr = extra_fields.EmailField()
    ministry: int = fields.IntField()
    public_authority: int = fields.IntField()
    topic: fields.ManyToManyRelation[RtiTopic] = fields.ManyToManyField(
        "models.RtiTopic", related_name="topic"
    )
    query: str = fields.CharField(max_length=512)
    filename: str = fields.CharField(max_length=253) #256-3
    response: fields.ForeignKeyRelation[Response] = fields.ForeignKeyField(
        "models.Response", related_name="response", null = True
    )
