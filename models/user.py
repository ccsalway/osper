from library.database import db


def get_user_by_username(username):
    """Gets a user by the username"""
    if not username: return None
    return db.execute("select * from users where username = ? limit 1", (username,)).fetchone()


def get_user_by_userid(userid):
    """Gets a user by the user ID"""
    if not userid: return None
    return db.execute("select * from users where userid = ? limit 1", (userid,)).fetchone()
