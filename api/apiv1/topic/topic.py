from typing import Any, List, Union
from api import deps
from fastapi import APIRouter, Depends, HTTPException
from schemas import topic
from models import RtiTopic
from slugify import slugify

router = APIRouter()


@router.get("/getall", response_model=List[topic.TopicOut])
async def get_all_topics():
    return await RtiTopic.all()


@router.post("/add", response_model=Union[topic.TopicOut, None])
async def create_topic(
    content: topic.TopicIn, current_user=Depends(deps.get_current_active_user)
) -> Union[RtiTopic, None]:

    if await RtiTopic.exists(topic_word=content.topic_word):
        raise HTTPException(404, detail="Topic already exists!")

    _kwargs = {
        "topic_word": content.topic_word,
        "topic_slug": slugify(content.topic_word),
        "created_by": current_user,
    }

    topicObj = await RtiTopic.create(**_kwargs)
    await topicObj.save()

    return topicObj


@router.delete("/delete")
async def create_topic(
    content: topic.TopicDeleteIn, current_user=Depends(deps.get_current_active_user)
) -> Any:

    if not await RtiTopic.exists(topic_slug=content.topic_slug):
        raise HTTPException(404, detail="Topic doesn't exists!")

    topicObj = await RtiTopic.get(topic_slug=content.topic_slug)
    await topicObj.delete()

    return {}
