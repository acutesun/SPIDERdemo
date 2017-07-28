import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect('MTime.db')
    cur = conn.execute('select * from MTIme')
    for i in cur.fetchall():
        print(i)