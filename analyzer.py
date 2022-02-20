import sqlite3
import matplotlib
from sys import platform

def get_data(path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute("select * from bibs")
        print(cur.fetchall())


if __name__ == "__main__":
    db_path = "/var/lib/bib-spaces-analyzer/spaces.db" if platform.startswith("linux") else "spaces.db"
    get_data(db_path)