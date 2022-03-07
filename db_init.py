#!/usr/bin/python3

import sqlite3
import os
from sys import platform

def init_db(path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE bibs (date DATETIME, bib_id, free_seats, status)''')
        con.commit()


if __name__ == "__main__":
    db_path = "/var/lib/bib-spaces-analyzer/spaces.db" if platform.startswith("linux") else "spaces.db"
    if os.path.isdir("/var/lib/bib-spaces-analyzer/") is False:
        os.mkdir("/var/lib/bib-spaces-analyzer/")
    init_db(db_path)
