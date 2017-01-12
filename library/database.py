import sqlite3


class DB(object):
    """Global library for accessing the database"""

    conn = None
    result = None

    def __init__(self):
        self.conn = sqlite3.connect('app.db', check_same_thread=False)
        self.conn.isolation_level = None  # autocommit
        self.conn.row_factory = sqlite3.Row  # dictionary results

    def execute(self, sql, args):
        cursor = self.conn.cursor()
        self.result = cursor.execute(sql, args)
        return self

    def fetchone(self):
        return self.result.fetchone()

    def fetchall(self):
        return self.result.fetchall()


db = DB()
