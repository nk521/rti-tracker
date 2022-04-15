from datetime import datetime

from pydantic import UUID4, EmailStr
from tortoise import fields, models

from models.file_upload import FileUpload
from models.response import Response
from models.topic import RtiTopic
from models.user import User
from models.utils import extra_fields


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
        "models.RtiTopic", related_name="topic", null=True
    )
    query: str = fields.CharField(max_length=512)
    file: fields.ForeignKeyRelation[FileUpload] = fields.ForeignKeyField(
        "models.FileUpload", related_name="file_rti", null=True
    )
    response: fields.ForeignKeyRelation[Response] = fields.ForeignKeyField(
        "models.Response", related_name="response", null=True
    )
