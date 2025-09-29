from typing import Optional, Type
from enum import Enum
import string
from secrets import choice
from datetime import datetime


def get_enum_label(enum_class: Type[Enum], value: int) -> Optional[str]:
    try:
        name = enum_class(value).name
        # Replace underscores with spaces or hyphens, then title-case it
        return name.replace("_", "-").title()
    except ValueError as e:
        return None


ALPHANUM = string.ascii_uppercase + string.digits


def generate_member_id(now: datetime | None = None) -> str:
    now = now or datetime.now()
    rand_txt = "".join(choice(ALPHANUM) for _ in range(6))
    date_txt = now.strftime("%Y%m%d")
    return f"{date_txt}-{rand_txt}"
