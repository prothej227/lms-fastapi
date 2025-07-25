from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.id'))
    full_name = Column(String(255))
    relationship_type = Column(String(255))
    dob = Column(Date)
    occupation = Column(String(255))
    employer = Column(String(255))

    member = relationship('Member', back_populates='beneficiaries')