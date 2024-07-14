from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate

from datetime import datetime, timedelta


async def get_contacts(
        skip: int,
        limit: int,
        user: User,
        db: Session) -> List[Contact]:
    """
    Retrieves a list of contacs for a specific user
      with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Note]
    """
    return db.query(Contact).filter(
        Contact.user_id == user.id
        ).offset(skip).limit(limit).all()


async def get_contact_id(
        contact_id: int,
        user: User,
        db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Note | None
    """
    return db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user.id
        ).first()


async def get_contact_name(
        contact_name: str,
        user: User,
        db: Session) -> List[Contact]:
    """
    Retrieves a single contact with the specified name for a specific user.

    :param contact_name: The name of the contact to retrieve.
    :type contact_name: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified name, or None if it does not exist.
    :rtype: Note | None
    """
    return db.query(Contact).filter(
        Contact.first_name == contact_name,
        Contact.user_id == user.id
        ).all()


async def get_contact_last_name(
        contact_last_name: str,
        user: User,
        db: Session) -> List[Contact]:
    """
    Retrieves a single contact with the specified last name
      for a specific user.

    :param contact_last_name: The name of the contact to retrieve.
    :type contact_last_name: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Note | None
    """
    return db.query(Contact).filter(
        Contact.last_name == contact_last_name,
        Contact.user_id == user.id
        ).all()


async def get_contact_email(contact_email: str,
                            user: User,
                            db: Session) -> Contact:
    """
    Retrieves a single contact with the specified email for a specific user.

    :param contact_email: The email of the contact to retrieve.
    :type contact_email: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified email,
      or None if it does not exist.
    :rtype: Note | None
    """
    return db.query(Contact).filter(
        Contact.email == contact_email,
        Contact.user_id == user.id
        ).first()


async def create_contact(body: ContactBase,
                         user: User,
                         db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactBase
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Note
    """
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birth_date=body.birth_date,
        additional_data=body.additional_data,
        created_at=body.created_at,
        user=user
        )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    print(f"Created Contact: {contact}")  # Debugging line
    return contact


async def remove_contact(contact_id: int,
                         user: User,
                         db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the note to remove.
    :type contact_id: int
    :param user: The user to remove the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Note | None
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user.id
    ).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(
        contact_id: int,
        body: ContactUpdate,
        user: User,
        db: Session) -> Contact | None:
    """
    Updates a single note with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Note | None
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user.id
        ).first()
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
    """
    Retrieves a list of contacts with upcoming birthdays .

    :param db: The database session.
    :type db: Session
    :return: The list of contacts with upcoming birthdays,
      or None if it does not exist.
    :rtype: Note | None
    """
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
