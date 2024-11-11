from typing import Optional, List
from datetime import timedelta, date

from sqlalchemy.orm import Session
from src.database.models import Contacts
from src.schemas import ContactModel

async def get_contacts(skip: int, limit: int, db: Session):
    return db.query(Contacts).offset(skip).limit(limit).all()

async def get_contact(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        db: Session = None
):
    query = db.query(Contacts)

    if first_name:
        query = query.filter(Contacts.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contacts.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contacts.email.ilike(f"%{email}%"))

    return query.first()

async def create_contact(body: ContactModel, db: Session):
    contact = Contacts(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        mobile_number=body.mobile_number,
        date_of_birth=body.date_of_birth,
        additional_notes=body.additional_notes,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactModel, db: Session):
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.mobile_number = body.mobile_number
        contact.date_of_birth = body.date_of_birth
        contact.additional_notes = body.additional_notes
        db.commit()
        db.refresh(contact)
    return contact

async def delete_contact(contact_id: int, db: Session):
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()#type: ignore
    if contact:
        db.delete(contact)
        db.commit()
    return contact


def get_upcoming_birthdays(db: Session) -> list[Contacts]:
    today = date.today()
    target_date = today + timedelta(days=7)

    upcoming_contacts = []

    contacts = db.query(Contacts).all()

    for contact in contacts:
        birth_date = contact.date_of_birth
        birthday_this_year = birth_date.replace(year=today.year)

        if today <= birthday_this_year <= target_date:
            upcoming_contacts.append(contact)

        elif today.month > birth_date.month or (today.month == birth_date.month and today.day > birth_date.day):
            birthday_next_year = birth_date.replace(year=today.year + 1)
            if today <= birthday_next_year <= target_date:
                upcoming_contacts.append(contact)

    return upcoming_contacts


