from typing import Any
from tortoise.fields import Field


class EmailField(Field, str):  # type: ignore
    """
    Email field.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.max_length = 256
        super().__init__(**kwargs)

    @property
    def SQL_TYPE(self) -> str:  # type: ignore
        return f"VARCHAR({self.max_length})"
