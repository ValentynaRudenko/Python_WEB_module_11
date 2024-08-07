from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.conf.config import settings
import redis

import pickle


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        Method of the Auth class. Verify password.

        :param plain_password: The plain_password.
        :type plain_password: str
        :param hashed_password: The hashed_password.
        :type hashed_password: str
        :return: plain_password, hashed_password.
        :rtype: Note | None
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
         Method of the Auth class. Get hashed password.

        :param password: The plain_password.
        :type password: str
        :return: hashed_password.
        :rtype: Note | None
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(
            self,
            data: dict,
            expires_delta: Optional[float] = None
            ):
        """
         Method of the Auth class. Create access token.

        :param data: Data.
        :type data: dict
        :param expires_delta: Expired time.
        :type expires_delta: float
        :return: encoded_access_token.
        :rtype: Note | None
        """
        to_encode = data.copy()
        if expires_delta:
            expire = (
                datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
            )
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(timezone.utc),
             "exp": expire,
             "scope": "access_token"}
             )
        encoded_access_token = jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
            )
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(
            self,
            data: dict,
            expires_delta: Optional[float] = None
            ):
        """
         Method of the Auth class. Create refresh token.

        :param data: Data.
        :type data: dict
        :param expires_delta: Expired time.
        :type expires_delta: float
        :return: encoded_refresh_token.
        :rtype: Note | None
        """
        to_encode = data.copy()
        if expires_delta:
            expire = (
                datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
            )
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.now(timezone.utc),
             "exp": expire,
             "scope": "refresh_token"}
             )
        encoded_refresh_token = jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
            )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
         Method of the Auth class. Decode refresh token.

        :param refresh_token: Refresh token.
        :type refresh_token: str
        :return: email.
        :rtype: Note | None
        """
        try:
            payload = jwt.decode(
                refresh_token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
                )
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid scope for token'
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials'
                )

    async def get_current_user(
            self,
            token: str = Depends(oauth2_scheme),
            db: Session = Depends(get_db)
            ):
        """
         Method of the Auth class. Get current user.

        :param token: token.
        :type token: str
        :param db: The database session.
        :type db: Session
        :return: user.
        :rtype: Note | None
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
                )
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user

    def create_email_token(self, data: dict):
        """
         Method of the Auth class. Create email token.

        :param data: data.
        :type data: dict
        :return: token.
        :rtype: Note | None
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        Method of the Auth class. Get email from token.

        :param token: token.
        :type token: str
        :return: email.
        :rtype: Note | None
        """
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
                )
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification"
                )


auth_service = Auth()
