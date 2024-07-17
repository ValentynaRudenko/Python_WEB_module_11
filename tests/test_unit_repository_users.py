import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import (
    UserModel, UserResponse, UserDb, TokenModel, RequestEmail
)
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user_data = {
            "email": "test@example.com",
            "password": "password"
        }
        self.user_model = UserModel(**self.user_data)
        self.user = User(**self.user_data)

    async def test_get_user_by_email_found(self):
        self.session.query().filter()\
            .first.return_value = self.user
        result = await get_user_by_email(
            email="test@example.com",
            db=self.session
            )
        self.assertEqual(result, self.user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(
            email="test@example.com",
            db=self.session
            )
        self.assertIsNone(result)

    async def test_create_user(self):
        self.session.add = MagicMock()
        self.session.commit = MagicMock()
        self.session.refresh = MagicMock()
        avatar_url = "http://example.com/avatar.png"

        with unittest.mock.patch(
            'src.repository.users.Gravatar'
             ) as mock_gravatar:
            mock_gravatar().get_image.return_value = avatar_url
            result = await create_user(
                body=self.user_model,
                db=self.session
                )
            self.assertEqual(result.email, self.user_model.email)
            self.assertEqual(result.avatar, avatar_url)
            self.session.add.assert_called_once_with(result)
            self.session.commit.assert_called_once()
            self.session.refresh.assert_called_once_with(result)

    async def test_update_token(self):
        new_token = "new_token"
        await update_token(
            user=self.user,
            token=new_token,
            db=self.session
            )
        self.assertEqual(self.user.refresh_token, new_token)
        self.session.commit.assert_called_once()

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        await confirmed_email(
            email="test@example.com",
            db=self.session
            )
        self.assertTrue(self.user.confirmed)
        self.session.commit.assert_called_once()

    async def test_update_avatar(self):
        new_avatar_url = "http://example.com/new_avatar.png"
        self.session.query().filter().first.return_value = self.user
        result = await update_avatar(
            email="test@example.com",
            url=new_avatar_url,
            db=self.session
            )
        self.assertEqual(result.avatar, new_avatar_url)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
