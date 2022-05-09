from typing import List
from models import FileUpload, Rti, RtiTopic, Response, User

from utils import utils
from faker import Faker
from tqdm.asyncio import tqdm
import asyncio
from slugify import slugify


class Populate:
    def __init__(self) -> None:
        self.fake: Faker = Faker()
        self.users = []
        self.topics = []
        self.files = []

    @classmethod
    async def init(cls):
        self = Populate()
        await self.update_lists()
        return self

    async def update_lists(self) -> None:
        self.users = await User.all()
        self.topics = await RtiTopic.all()
        self.files = await FileUpload.all()

    async def populate_user(self, amount: int = 10) -> None:
        async for _ in tqdm(range(amount), desc="Populating users"):
            _kwargs = {
                "username": (username := self.get_username()),
                "email": self.fake.email(),
                "hashed_password": utils.GetPasswordHash(username),
                "is_active": True,
                "is_superuser": True,
                "full_name": self.fake.name(),
                # "deleted": self.fake.boolean(),
            }
            userObj = await User.create(**_kwargs)
            await userObj.save()

        self.users = await User.all()

    async def populate_file_upload(self, amount: int = 10) -> None:
        async for _ in tqdm(range(amount), desc="Populating file uploads"):
            _kwargs = {
                "path": self.fake.file_path(depth=4, extension="pdf"),
                "filename": (filename := f"{self.fake.uuid4()}.pdf"),
                "path": f"uploads/{filename}",
                "created_by": self.fake.random_choices(self.users, 1)[0],
            }

            fileUploadObj = await FileUpload.create(**_kwargs)
            await fileUploadObj.save()

        self.files = await FileUpload.all()

    async def populate_topic(self, topics: List[str] = None) -> None:
        if not topics:
            topics = [
                "Internet Shutdowns",
                "Litigation",
                "Free Speech",
                "Hakuna Matata",
                "Damn It's Cold",
            ]

        async for topic in tqdm(topics, desc="Populating topics"):
            _kwargs = {
                "topic_word": topic,
                "topic_slug": slugify(topic),
                "created_by": self.fake.random_choices(self.users, 1)[0],
            }

            rtiTopicObj = await RtiTopic.create(**_kwargs)
            await rtiTopicObj.save()

        self.topics = await RtiTopic.all()

    async def populate_rti(self, amount: int = 10, response: bool = True) -> None:
        async for _ in tqdm(range(amount), desc="Populating RTIs"):
            _kwargs = {
                "rti_send_date": int(self.fake.date_time_this_century().timestamp()),
                "registration_number": f"{self.fake.random_number(4)}/{self.fake.random_number(2)}/{self.fake.random_number(5)}",
                "name_of_sender": self.fake.random_choices(self.users, 1)[0],
                "title": self.fake.sentence(),
                "email_of_sender": self.fake.email(),
                "query": self.fake.sentence(nb_words=15, variable_nb_words=False),
                "ministry": self.fake.random_number(2),
                "public_authority": self.fake.random_number(3),
                "created_by": self.fake.random_choices(self.users, 1)[0],
                "file": self.fake.random_choices(self.files, 1)[0],
                "draft": self.fake.boolean(),
                # "response": "",
            }
            rtiObj = await Rti.create(**_kwargs)

            for topic in list(set(self.fake.random_choices(self.topics))):
                await rtiObj.topic.add(topic)

            if response:
                if self.fake.boolean:
                    responseObj = await Response.create(
                        created_by=self.fake.random_choices(self.users, 1)[0],
                        file=self.fake.random_choices(self.files, 1)[0],
                        response_recv_date=int(
                            self.fake.date_time_this_century().timestamp()
                        ),
                    )
                    await responseObj.save()
                    rtiObj.response = responseObj

            await rtiObj.save()

    def get_username(self, max_length: int = 15) -> str:
        while True:
            if len(x := self.fake.user_name()) <= max_length:
                return x
