from typing import Optional, Type
from enum import Enum


def get_enum_label(enum_class: Type[Enum], value: int) -> Optional[str]:
    try:
        name = enum_class(value).name
        # Replace underscores with spaces or hyphens, then title-case it
        return name.replace("_", "-").title()
    except ValueError as e:
        return None
