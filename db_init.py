import sqlite3

def init_db(path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE bibs (year, month, day, hour, minute, bib_id, free_seats, status)''')
        con.commit()


if __name__ == "__main__":
    init_db("test-0.db")