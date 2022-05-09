from typing import Union
import toml
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User

config = toml.load("config.toml")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/apiv1/auth/session")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # TODO: not the proper way to achieve this
    # Someone must rewrite OAuth2PasswordBearer class and override __call__
    # to return "False" instead of raising HTTPException error when
    # the user isn't logged in.

    # try:
    #     token: str = await oauth2_scheme(request)
    # except HTTPException:
    #     return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config["jwt"]["key"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.get(username=username)
    if user is None:
        raise credentials_exception

    if user.deleted:
        raise credentials_exception

    return user


def get_current_active_user(curr_user: User = Depends(get_current_user)) -> User:
    if not curr_user.is_active:
        raise HTTPException(status_code=403, detail="User is not active.")

    return curr_user


def get_current_superuser(curr_user: User = Depends(get_current_user)) -> User:
    if not curr_user.is_superuser:
        raise HTTPException(status_code=403, detail="User doesn't have privileges.")

    return curr_user


async def get_current_user_no_raise(
    token: str = Depends(oauth2_scheme),
) -> Union[User, bool]:
    try:
        payload = jwt.decode(token, config["jwt"]["key"])
        username: str = payload.get("sub")
        if username is None:
            return False
    except JWTError:
        return False

    user = await User.get(username=username)
    if user is None:
        return False

    if user.deleted:
        return False

    return user


def get_current_active_user_no_raise(
    curr_user: User = Depends(get_current_user_no_raise),
) -> Union[User, bool]:
    breakpoint()
    if not curr_user:
        return False

    if not curr_user.is_active:
        raise HTTPException(status_code=403, detail="User is not active.")

    return curr_user


def get_current_superuser_no_raise(
    curr_user: User = Depends(get_current_user),
) -> Union[User, bool]:
    if not curr_user:
        return False

    if not curr_user.is_superuser:
        raise HTTPException(status_code=403, detail="User doesn't have privileges.")

    return curr_user
