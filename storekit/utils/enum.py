from enum import Enum
from enum import IntEnum as LibIntEnum


class IntEnum(LibIntEnum):
    """Enum where members are also (and must be) ints"""

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            description=f"An enumeration: {' '.join(f'{i.name}={i.value}' for i in cls)}",
        )


class StrEnum(str, Enum):
    """Enum where members are also (and must be) strings"""

    def __str__(self) -> str:
        return self.value

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            description=f"An enumeration: {' '.join(f'{i.name}={i.value}' for i in cls)}",
        )
