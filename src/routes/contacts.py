from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponseModel
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/all", response_model=List[ContactResponseModel])
async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/", response_model=ContactResponseModel)
async def get_contact(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    contact = await repository_contacts.get_contact(first_name, last_name, email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/upcoming_birthdays", response_model=List[ContactResponseModel])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    upcoming_contacts = repository_contacts.get_upcoming_birthdays(db)
    return upcoming_contacts


@router.post("/contact", response_model=ContactResponseModel)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponseModel)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponseModel)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
