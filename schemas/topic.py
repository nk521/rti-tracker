from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr


class TopicIn(BaseModel):
    topic_word: str

class TopicOut(BaseModel):
    id: UUID4
    topic_word: str
    topic_slug: str

class TopicDeleteIn(BaseModel):
    topic_slug: Optional[str]