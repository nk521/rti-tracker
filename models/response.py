from datetime import datetime

from pydantic import UUID4
from tortoise import fields, models

from models.file_upload import FileUpload
from models.user import User
from models.utils import extra_fields


class Response(models.Model):
    id: UUID4 = fields.UUIDField(pk=True)
    created_on: datetime = fields.DatetimeField(auto_now_add=True)
    updated_on: datetime = fields.DatetimeField(auto_now=True)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="creator_response"
    )
    response_recv_date = extra_fields.DatetimeTimestampField()
    file: fields.ForeignKeyRelation[FileUpload] = fields.ForeignKeyField(
        "models.FileUpload", related_name="file_response", null=True
    )
