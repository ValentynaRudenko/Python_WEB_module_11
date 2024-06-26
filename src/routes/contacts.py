from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository.contacts import (
    get_contact_id, get_contacts, create_contact, remove_contact,
    update_contact, get_contact_name, get_contact_last_name, get_contact_email,
    get_upcoming_birthdays
)


router = APIRouter(prefix='/contacts')


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
        ):
    contacts = await get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact_id(
    contact_id: int,
    db: Session = Depends(get_db)
        ):
    contact = await get_contact_id(contact_id, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.get("/name/{contact_name}", response_model=List[ContactResponse])
async def read_contact_name(
    contact_name: str,
    db: Session = Depends(get_db)
        ):
    contact = await get_contact_name(contact_name, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.get(
        "/last_name/{contact_last_name}", response_model=List[ContactResponse]
        )
async def read_contact_last_name(
    contact_last_name: str,
    db: Session = Depends(get_db)
        ):
    contact = await get_contact_last_name(contact_last_name, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.get("/email/{contact_email}", response_model=ContactResponse)
async def read_contact_email(
    contact_email: str,
    db: Session = Depends(get_db)
        ):
    contact = await get_contact_email(contact_email, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact_route(
    body: ContactBase,
    db: Session = Depends(get_db)
        ):
    return await create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact_route(
    body: ContactUpdate,
    contact_id: int,
    db: Session = Depends(get_db)
        ):
    contact = await update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact_route(
    contact_id: int,
    db: Session = Depends(get_db)
        ):
    contact = await remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/birthdays/", response_model=List[ContactResponse])
async def read_upcoming_birthdays(
    db: Session = Depends(get_db)
        ):
    contacts = await get_upcoming_birthdays(db)
    return contacts
