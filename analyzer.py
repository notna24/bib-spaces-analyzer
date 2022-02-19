import sqlite3
import matplotlib

def get_data(path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute("select * from bibs")
        print(cur.fetchall())


if __name__ == "__main__":
    get_data("test-0.db")