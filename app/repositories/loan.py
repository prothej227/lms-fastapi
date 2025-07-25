from sqlalchemy.orm import Session
from app.models.loan import Loan, LoanStatus
from app.models.loan_type import LoanType
from app.models.loan_activity import LoanActivity
from app.models.loan_application import LoanApplication

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_loan(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def get_loan(self, loan_id: int) -> Loan:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def update_loan(self, loan: Loan) -> Loan:
        existing_loan = self.get_loan(loan.id)
        if existing_loan:
            for key, value in loan.__dict__.items():
                setattr(existing_loan, key, value)
            self.db.commit()
            self.db.refresh(existing_loan)
            return existing_loan
        return None

    def delete_loan(self, loan_id: int) -> bool:
        loan = self.get_loan(loan_id)
        if loan:
            self.db.delete(loan)
            self.db.commit()
            return True
        return False

    def create_loan_type(self, loan_type: LoanType) -> LoanType:
        self.db.add(loan_type)
        self.db.commit()
        self.db.refresh(loan_type)
        return loan_type

    def get_loan_type(self, name: str) -> LoanType:
        return self.db.query(LoanType).filter(LoanType.name == name).first()

    def create_loan_activity(self, activity: LoanActivity) -> LoanActivity:
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_loan_activity(self, activity_id: int) -> LoanActivity:
        return self.db.query(LoanActivity).filter(LoanActivity.id == activity_id).first()

    def create_loan_application(self, application: LoanApplication) -> LoanApplication:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_loan_application(self, application_id: int) -> LoanApplication:
        return self.db.query(LoanApplication).filter(LoanApplication.id == application_id).first()