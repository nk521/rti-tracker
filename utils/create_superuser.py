from pydantic import EmailStr
from models import User
from utils import utils


async def util_create_superuser(
    username: str, email: EmailStr, password: str, full_name: str
) -> None:
    await utils.init_tortoise()
    userObj = await User.create(
        full_name=full_name,
        username=username,
        email=email,
        hashed_password=utils.GetPasswordHash(password),
        is_active=True,
        is_superuser=True,
    )
    await userObj.save()
    print(f"Created a new superadmin: {userObj.username}<{userObj.email}>!")
