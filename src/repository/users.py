from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a single user with the specified email.

    :param email: The email of the contact to retrieve.
    :type contact_email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email, or None if it does not exist.
    :rtype: Note | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    :param body: The data for the User to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: Note
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Refresh token.

    :param user: The user to update the token for.
    :type user: User
    :param token: The current token.
    :type body: str
    :param db: The database session.
    :type db: Session
    :return: The newly created token.
    :rtype: Note
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    To confirm the user by email.

    :param email: The email to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The newly created token.
    :rtype: Note
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    To update the user's avatar.

    :param email: The email of the user to update avatar.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The newly created token.
    :rtype: Note
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
