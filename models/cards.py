import time
from datetime import datetime, timedelta

from library.database import db


def get_cards_by_accountid(accid):
    """Gets a list of cards associated to an account"""
    if not accid: return None
    return db.execute("select * from cards where accid = ? order by owner", (accid,)).fetchall()


def get_card_by_id(accid, cardid):
    """Gets a card by it's ID, with a security check against the account"""
    if not accid or not cardid: return None
    return db.execute("select * from cards where accid = ? and cardid = ? limit 1", (accid, cardid)).fetchone()


def get_card_topups(cardid, start_date):
    """Gets a list of card top-ups from a defined start date"""
    if not cardid or not start_date: return None
    return db.execute("select sum(amount) from topups where cardid = ? and timestamp >= ?", (cardid, start_date)).fetchone()


def increase_card_balance(cardid, amount):
    """Increases the balance on a card and logs the top-up"""
    if not cardid or not amount: return None
    db.execute("update cards set balance = balance + ? where cardid = ? limit 1", (amount, cardid))
    topup_time = int(time.mktime(datetime.utcnow().timetuple()))
    db.execute("insert into topups (cardid, timestamp, amount) VALUES (?, ?, ?)", (cardid, topup_time, amount))


def compliance_checks(card):
    """Checks top-up limits are within regulations"""
    if not card: return None

    available = 500  # maximum amount allowed in a day
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # - maximum balance at any time 1000
    if card['balance'] >= 1000:
        raise UserWarning("You have reached the cards maximum allowed balance")

    # - maximum 500 worth of loads per day
    start_date = int(time.mktime(today.timetuple()))
    result = get_card_topups(card['cardid'], start_date)
    if result[0]:
        if result[0] >= 500:
            raise UserWarning("You have reached the daily top-up limit")
        else:
            available = 500 - result[0]

    # - maximum 800 worth of loads per 30 days
    start_date = int(time.mktime((today - timedelta(days=30)).timetuple()))
    result = get_card_topups(card['cardid'], start_date)
    if result[0] and result[0] >= 800:
        raise UserWarning("You have already exceeded the 30 day top-up limit")

    # - maximum 2000 worth of loads per 365 days
    start_date = int(time.mktime((today - timedelta(days=365)).timetuple()))
    result = get_card_topups(card['cardid'], start_date)
    if result[0] and result[0] >= 2000:
        raise UserWarning("You have already exceeded the 365 day top-up limit")

    return available
