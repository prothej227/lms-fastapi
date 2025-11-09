from app.services.crud import CrudService
from app.schemas import loan_management as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Loan
from app.repositories.loan_management.loan import LoanRepository
from typing import List, Dict
from dateutil.relativedelta import relativedelta
import math
from app.utils.helpers import extract_suffix_int


class LoanService(CrudService[Loan, schemas.loan.LoanCreate, schemas.loan.LoanUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Loan, LoanRepository, db)

    async def create_amortization_schedule(self, loan_id) -> List[Dict]:
        loan: Loan = await self.get_by_id(
            id=loan_id,
            relationships=["loan_activities"],
        )

        if not loan:
            raise ValueError(f"Loan {loan_id} not found.")

        principal = float(loan.amount)
        annual_rate = float(loan.interest_rate)
        start_date = loan.start_date
        end_date = loan.end_date

        term_months = (end_date.year - start_date.year) * 12 + (
            end_date.month - start_date.month
        )
        if term_months <= 0:
            raise ValueError("Invalid loan term. End date must be after start date.")

        monthly_rate = (annual_rate / 100) / 12
        if monthly_rate > 0:
            monthly_payment = (
                principal
                * (monthly_rate * math.pow(1 + monthly_rate, term_months))
                / (math.pow(1 + monthly_rate, term_months) - 1)
            )
        else:
            monthly_payment = principal / term_months

        monthly_payment = round(monthly_payment, 2)

        # Gather payments by installment reference
        payments: Dict[int, float] = {}
        for act in loan.loan_activities:
            suffix = extract_suffix_int(act.reference_number)
            if suffix:
                payments[suffix] = payments.get(suffix, 0.0) + float(act.amount)

        schedule: List[Dict] = []
        balance = principal
        cumulative_paid = 0.0

        for i in range(1, term_months + 1):
            paid_amount = payments.get(i, 0.0)
            interest_due = balance * monthly_rate
            principal_due = monthly_payment - interest_due

            # Determine how much of the actual payment goes to principal
            principal_paid = max(0.0, paid_amount - interest_due)
            balance = max(0.0, balance - principal_paid)

            cumulative_paid += paid_amount
            current_remaining_balance = max(0.0, principal - cumulative_paid)
            due_date = start_date + relativedelta(months=i)

            if paid_amount >= round(monthly_payment, 2):
                status = "Paid"
            elif 0 < paid_amount < monthly_payment:
                status = "Partially Paid"
            else:
                status = "Unpaid"

            schedule.append(
                {
                    "installment_no": i,
                    "due_date": due_date,
                    "payment_amount": monthly_payment,
                    "principal_component": round(principal_due, 2),
                    "interest_component": round(interest_due, 2),
                    "remaining_balance": round(balance, 2),
                    "current_remaining_balance": round(current_remaining_balance, 2),
                    "status": status,
                    "paid_amount": round(paid_amount, 2),
                }
            )

        return schedule
