from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    middle_name = Column(String(255))
    last_name = Column(String(255))
    birth_address = Column(String(255))
    dob = Column(Date)
    nationality = Column(String(255))
    religion = Column(String(255))
    sex = Column(String(6))
    civil_status = Column(String(50))
    current_address = Column(String(255))
    permanent_address = Column(String(255))
    contact_number = Column(String(20))
    zip_code = Column(String(10))
    tin_number = Column(String(40))
    id_type1 = Column(String(25))
    id_type2 = Column(String(25))
    id_number1 = Column(String(30))
    id_number2 = Column(String(30))
    basic_education = Column(String(255))
    vocational_degree = Column(String(255))
    college_degree = Column(String(255))
    pos_grad_degree = Column(String(255))
    occupation = Column(String(10))

    beneficiaries = relationship('Beneficiary', back_populates='member')
    loans = relationship('Loan', back_populates='member')