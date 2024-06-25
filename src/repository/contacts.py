from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.models import Contact
from src.schemas import ContactBase, ContactUpdate

from datetime import datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact_id(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contact_name(contact_name: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.first_name == contact_name).all()


async def get_contact_last_name(
        contact_last_name: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(
        Contact.last_name == contact_last_name).all()


async def get_contact_email(contact_email: str, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.email == contact_email).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birth_date=body.birth_date,
        additional_data=body.additional_data,
        created_at=body.created_at
        )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    print(f"Created Contact: {contact}")  # Debugging line
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(
        contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone = body.phone,
        contact.birth_date = body.birth_date,
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = datetime.now()
    today_date = today.date()
    next_week_date = today_date + timedelta(days=7)
    month_day_today = today.strftime('%m%d')
    month_day_next_week = next_week_date.strftime('%m%d')

    month_day_contact = func.concat(
        func.to_char(Contact.birth_date, "MM"),
        func.to_char(Contact.birth_date, "DD")
    )

    return db.query(Contact).filter(
        (month_day_contact >= month_day_today) &
        (month_day_contact <= month_day_next_week)
        ).all()
