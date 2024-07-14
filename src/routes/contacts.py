from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
# from fastapi_limiter import RateLimiter
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository.contacts import (
    get_contact_id, get_contacts, create_contact, remove_contact,
    update_contact, get_contact_name, get_contact_last_name, get_contact_email,
    get_upcoming_birthdays
)
from src.services.auth import auth_service
from src.database.models import Contact, User

router = APIRouter(prefix='/contacts')


@router.get("/",
            response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
     ):
    """
    Retrieves a list of contacs for a specific user
      with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: A list of contacts.
    :rtype: List[Note]
    """
    contacts = await get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Note | None
    """
    contact = await get_contact_id(contact_id, current_user, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.get("/name/{contact_name}", response_model=List[ContactResponse])
async def read_contact_name(
    contact_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Retrieves a single contact with the specified name for a specific user.

    :param contact_name: The name of the contact to retrieve.
    :type contact_name: str
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The contact with the specified name, or None if it does not exist.
    :rtype: Note | None
    """
    contact = await get_contact_name(contact_name, current_user, db)
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
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Retrieves a single contact with the specified last name
      for a specific user.

    :param contact_last_name: The name of the contact to retrieve.
    :type contact_last_name: str
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Note | None
    """
    contact = await get_contact_last_name(contact_last_name, current_user, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.get("/email/{contact_email}", response_model=ContactResponse)
async def read_contact_email(
    contact_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Retrieves a single contact with the specified email for a specific user.

    :param contact_email: The email of the contact to retrieve.
    :type contact_email: str
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The contact with the specified email,
      or None if it does not exist.
    :rtype: Note | None
    """
    contact = await get_contact_email(contact_email, current_user, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found")
    return contact


@router.post("/",
             response_model=ContactResponse,
             status_code=status.HTTP_201_CREATED)
async def create_contact_route(
    body: ContactBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactBase
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The newly created contact.
    :rtype: Note
    """
    return await create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact_route(
    body: ContactUpdate,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Updates a single note with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The updated contact, or None if it does not exist.
    :rtype: Note | None
    """
    contact = await update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact_route(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the note to remove.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: The removed contact, or None if it does not exist.
    :rtype: Note | None
    """
    contact = await remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/birthdays/", response_model=List[ContactResponse])
async def read_upcoming_birthdays(
    db: Session = Depends(get_db)
        ):
    """
    Retrieves a list of contacts with upcoming birthdays.

    :param db: The database session.
    :type db: Session
    :return: The list of contacts with upcoming birthdays,
      or None if it does not exist.
    :rtype: Note | None
    """
    contacts = await get_upcoming_birthdays(db)
    return contacts
