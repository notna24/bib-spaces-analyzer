import sqlite3
from sys import platform

def init_db(path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE bibs (year, month, day, hour, minute, bib_id, free_seats, status)''')
        con.commit()


if __name__ == "__main__":
    db_path = "/var/lib/bib-spaces-analyzer/spaces.db" if platform.startswith("linux") else "spaces.db"
    init_db("test-0.db")