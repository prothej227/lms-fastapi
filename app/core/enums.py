from enum import Enum
from typing import Type, List


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
