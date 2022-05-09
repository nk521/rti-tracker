from datetime import datetime

from pydantic import UUID4
from tortoise import fields, models

from models.user import User


class FileUpload(models.Model):
    id: UUID4 = fields.UUIDField(pk=True)
    path = fields.CharField(max_length=500)
    filename: str = fields.CharField(max_length=253)
    created_on: datetime = fields.DatetimeField(auto_now_add=True)
    updated_on: datetime = fields.DatetimeField(auto_now=True)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="creator_file_upload"
    )
