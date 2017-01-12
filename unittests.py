import time
from datetime import datetime, timedelta

from unittest import TestCase

from models.user import *
from models.login import *
from models.cards import *
from models.payment import *


class TestModelUser(TestCase):
    def test_get_user_by_username(self):
        self.assertIsNotNone(get_user_by_username('paul@smith.com'))
        self.assertIsNone(get_user_by_username('no@one.com'))

    def test_get_user_by_userid(self):
        self.assertIsNotNone(get_user_by_userid(1))


class TestModelLogin(TestCase):
    def test_access_token(self):
        access_token = create_access_token(1)
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(check_user_login(access_token))


class TestModelCards(TestCase):
    def test_get_cards_by_accountid(self):
        self.assertIsNotNone(get_cards_by_accountid(1))

    def test_get_card_by_id(self):
        self.assertIsNotNone(get_card_by_id(1, 1))

    def test_get_card_topups(self):
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = int(time.mktime((today - timedelta(days=30)).timetuple()))
        self.assertIsNotNone(get_card_topups(1, start_date))

    def test_increase_card_balance(self):
        self.assertIsNone(increase_card_balance(1, 1))

    def test_compliance_checks(self):
        card = get_card_by_id(1, 2)
        self.assertIsInstance(compliance_checks(card), int)


class TestModelPayment(TestCase):
    def test_public_auth_token(self):
        self.assertIsNotNone(payment.public_auth_token())

    def test_sale_nonce(self):
        pass
