from pydantic import BaseModel, EmailStr
from datetime import date

class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    date_of_birth: date
    additional_notes: str | None = None

class ContactResponseModel(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True