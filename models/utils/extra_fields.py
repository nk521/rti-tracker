from typing import Any, Optional, Type, Union
from tortoise import ConfigurationError, Model
from tortoise.fields import Field
import datetime
from ciso8601 import parse_datetime
from tortoise import timezone
import warnings
from tortoise.timezone import get_timezone, get_use_tz, localtime

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


class DatetimeTimestampField(Field, datetime.datetime):
    """
    Datetime field.

    ``auto_now`` and ``auto_now_add`` is exclusive.
    You can opt to set neither or only ONE of them.

    ``auto_now`` (bool):
        Always set to ``datetime.utcnow()`` on save.
    ``auto_now_add`` (bool):
        Set to ``datetime.utcnow()`` on first save only.
    """

    SQL_TYPE = "TIMESTAMP"

    class _db_mysql:
        SQL_TYPE = "DATETIME(6)"

    class _db_postgres:
        SQL_TYPE = "TIMESTAMPTZ"

    def __init__(self, auto_now: bool = False, auto_now_add: bool = False, **kwargs: Any) -> None:
        if auto_now_add and auto_now:
            raise ConfigurationError("You can choose only 'auto_now' or 'auto_now_add'")
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_python_value(self, value: Any) -> Optional[int]:
        if value is None:
            value = None
        else:
            if isinstance(value, datetime.datetime):
                value = int(value.timestamp())
            elif isinstance(value, int):
                value = value
            else:
                value = int(parse_datetime(value).timestamp())
            
            # if timezone.is_naive(datetime.datetime.fromtimestamp(value)):
            #     value = int(timezone.make_aware(datetime.datetime.fromtimestamp(value), get_timezone()).timestamp())
            # else:
            #     value = int(localtime(value).timestamp())
        self.validate(value)
        return value

    def to_db_value(
        self, value: Optional[int], instance: "Union[Type[Model], Model]"
    ) -> Optional[datetime.datetime]:

        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = timezone.now()
            setattr(instance, self.model_field_name, value)
            return value
        if value is not None:
            value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            if get_use_tz():
                if timezone.is_naive(value):
                    warnings.warn(
                        "DateTimeField %s received a naive datetime (%s)"
                        " while time zone support is active." % (self.model_field_name, value),
                        RuntimeWarning,
                    )
                    value = timezone.make_aware(value, "UTC")
        self.validate(value)
        return value

    @property
    def constraints(self) -> dict:
        data = {}
        if self.auto_now_add:
            data["readOnly"] = True
        return data

    def describe(self, serializable: bool) -> dict:
        desc = super().describe(serializable)
        desc["auto_now_add"] = self.auto_now_add
        desc["auto_now"] = self.auto_now
        return desc
