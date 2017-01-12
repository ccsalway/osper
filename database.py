import sqlite3

conn = sqlite3.connect('app.db')

c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS accounts (accid int)''')

c.execute('''CREATE TABLE IF NOT EXISTS users (accid int, userid int, username text, password text)''')

c.execute('''CREATE TABLE IF NOT EXISTS cards (accid int, cardid int, owner text, tail int, balance double)''')

c.execute('''CREATE TABLE IF NOT EXISTS topups (cardid int, timestamp int, amount double)''')

c.execute('''CREATE TABLE IF NOT EXISTS logins (userid int, timestamp int, token text)''')


c.execute('''INSERT INTO accounts (accid) VALUES (1)''')

c.execute('''INSERT INTO users (accid, userid, username, password) VALUES (1, 1, 'paul@smith.com', '$2b$12$dilEr7.RWqCNpaX/6eNThumP.yjDV8RcRyAXfOdzsN8Q41GbHbJ4K')''')

c.execute('''INSERT INTO cards (accid, cardid, owner, tail, balance) VALUES (1, 1, 'Ben', 8273, 0.00)''')

c.execute('''INSERT INTO cards (accid, cardid, owner, tail, balance) VALUES (1, 2, 'Susan', 7642, 0.00)''')


conn.commit()
conn.close()
