from enum import Enum
from typing import Type, List

class BaseEnum(Enum):
    @classmethod
    def from_str(cls, name: str):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(f"{cls.__name__} does not have a member named '{name}'")
        
class PaymentFrequency(Enum):
    MONTHLY = 1
    QUARTERLY = 2
    SEMI_ANNUAL = 3
    ANNUAL = 4


class AmortizationType(Enum):
    EQUAL_INSTALLMENTS = 1
    REDUCING_BALANCE = 2
    BULLET_PAYMENT = 3


REF_ENUMS: dict[str, Type[Enum]] = {
    "payment_frequency": PaymentFrequency,
    "amortization_type": AmortizationType,
}

HYPEN_LABELS: List[str] = ["SEMI_ANNUAL"]
