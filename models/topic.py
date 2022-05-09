from tortoise import fields, models
from models.user import User


class RtiTopic(models.Model):
    id = fields.UUIDField(pk=True)
    topic_word = fields.CharField(max_length=256, unique=True)
    topic_slug = fields.CharField(max_length=300, unique=True)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="creator_topic"
    )
    created_on = fields.DatetimeField(auto_now_add=True)
    updated_on = fields.DatetimeField(auto_now=True)
