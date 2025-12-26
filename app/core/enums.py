from enum import Enum
from typing import Type, List


class BaseEnum(Enum):
    @classmethod
    def from_str(cls, name: str):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(f"{cls.__name__} does not have a member named '{name}'")

    def __str__(self):
        return self.name

    def get_proper_name(self):
        return self.name.replace("_", " ").title()


class LoanActivityType(BaseEnum):
    DISBURSEMENT = 1
    PAYMENT = 2
    PENALTY = 3
    INTEREST = 4
    ADJUSTMENT = 5
    WRITE_OFF = 6


class LoanActivityStatus(BaseEnum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    POSTED = 4


class PaymentFrequency(BaseEnum):
    MONTHLY = 1
    QUARTERLY = 2
    SEMI_ANNUAL = 3
    ANNUAL = 4


class LoanStatus(BaseEnum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3
    SUSPENDED = 4
    DEFAULTED = 5


class LoanApplicationStatus(BaseEnum):
    SUBMITTED = 1
    UNDER_REVIEW = 2
    APPROVED = 3
    REJECTED = 4
    WITHDRAWN = 5


class AmortizationType(BaseEnum):
    EQUAL_INSTALLMENTS = 1
    REDUCING_BALANCE = 2
    BULLET_PAYMENT = 3


REF_ENUMS: dict[str, Type[Enum]] = {
    "payment_frequency": PaymentFrequency,
    "amortization_type": AmortizationType,
    "loan_status": LoanStatus,
    "loan_application_status": LoanApplicationStatus,
}

HYPEN_LABELS: List[str] = ["SEMI_ANNUAL"]
