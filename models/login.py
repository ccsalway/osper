import time
from datetime import datetime
from uuid import uuid4

from library.database import db
from user import get_user_by_userid


def create_access_token(userid):
    """Generates an access token and stores it in the database for future reference"""
    if not userid: return None
    access_token = uuid4().get_hex()
    access_time = int(time.mktime(datetime.utcnow().timetuple()))
    db.execute("insert into logins (userid, timestamp, token) VALUES (?,?,?)", (userid, access_time, access_token))
    return access_token


def check_user_login(access_token):
    """Checks an access token against the database and returns the associated user"""
    if not access_token: return None
    login = db.execute("select * from logins where token = ? limit 1", (access_token,)).fetchone()
    if not login: return None
    return get_user_by_userid(login['userid'])
