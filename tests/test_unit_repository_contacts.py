import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import (
    ContactBase, ContactUpdate
)
from src.repository.contacts import (
    get_contacts,
    get_contact_id,
    create_contact,
    remove_contact,
    update_contact,

)

import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit()\
            .all.return_value = contacts
        result = await get_contacts(
            skip=0, limit=10, user=self.user, db=self.session
            )
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter()\
            .first.return_value = contact
        result = await get_contact_id(
            contact_id=1, user=self.user, db=self.session
            )
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact_id(
            contact_id=1, user=self.user, db=self.session
            )
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactBase(
            first_name="test_first_name",
            last_name="test_last_name",
            email="test@example.com",
            phone=111111111,
            birth_date="2020-07-13",
            additional_data="test_additional_data",
            created_at="2024-07-13",
        )
        self.session.add = MagicMock()
        self.session.commit = MagicMock()
        self.session.refresh = MagicMock()
        result = await create_contact(
            body=body,
            user=self.user,
            db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birth_date, body.birth_date)
        self.assertEqual(result.created_at, body.created_at)
        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter()\
            .first.return_value = contact
        result = await remove_contact(
            contact_id=1,
            user=self.user,
            db=self.session)
        self.assertEqual(result, contact)
        self.session.delete.assert_called_once_with(contact)
        self.session.commit.assert_called_once()

    async def test_remove_contact_not_found(self):
        self.session.query().filter()\
            .first.return_value = None
        result = await remove_contact(
            contact_id=1,
            user=self.user,
            db=self.session
            )
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactUpdate(
            first_name="test_first_name",
            last_name="test_last_name",
            email="test@example.com",
            phone=111111111,
            birth_date="2020-07-13",
            additional_data="test_additional_data",
            created_at="2024-07-13"
            )
        contact = Contact(user=self.user)
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1,
            body=body,
            user=self.user,
            db=self.session
            )
        self.assertEqual(result, contact)
        self.session.commit.assert_called_once()

    async def test_update_contact_not_found(self):
        body = ContactUpdate(
            first_name="test_first_name",
            last_name="test_last_name",
            email="test@example.com",
            phone=111111111,
            birth_date="2020-07-13",
            additional_data="test_additional_data",
            created_at="2024-07-13"
            )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1,
            body=body,
            user=self.user,
            db=self.session
            )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
