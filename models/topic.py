from tortoise import fields, models
from slugify import slugify

class RtiTopic(models.Model):
    id = fields.UUIDField(pk=True)
    topic_word = fields.TextField()
    topic_slug = fields.TextField()
    created_on = fields.DatetimeField(auto_now_add=True)
    updated_on = fields.DatetimeField(auto_now=True)

    async def save(self, *args, **kwargs) -> None:
        self.topic_slug = slugify(self.topic_word)
        await super().save(*args, **kwargs)

