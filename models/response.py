from datetime import datetime

from pydantic import UUID4, EmailStr
from tortoise import fields, models

from models.file_upload import FileUpload
from models.topic import RtiTopic
from models.user import User


class Response(models.Model):
    id: UUID4 = fields.UUIDField(pk=True)
    created_on: datetime = fields.DatetimeField(auto_now_add=True)
    updated_on: datetime = fields.DatetimeField(auto_now=True)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="creator_response"
    )
    response_recv_date: datetime = fields.DatetimeField()
    file: fields.ForeignKeyRelation[FileUpload] = fields.ForeignKeyField(
        "models.FileUpload", related_name="file_response", null=True
    )
