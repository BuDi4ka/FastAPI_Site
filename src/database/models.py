from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contacts(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    mobile_number = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    additional_notes = Column(String(500), nullable=True)

