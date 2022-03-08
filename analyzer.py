#!/usr/bin/python3

from configparser import RawConfigParser
import time
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sys import platform


def find_least_visit_times(weeks):
	pass

def plot_timeinterval(path, start, end, bibs):
    #this function plots a the spaces in a certain time interval
    data = {}
    for bib in bibs:
        raw_data = get_data(path, start, end, bib)
        data[bib] = ([i[0] for i in raw_data], [i[2] for i in raw_data])
    fig, ax = plt.subplots()
    for bib, t_s in data.items():
        ax.plot(t_s[0], t_s[1], label=bib)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.legend()
    plt.savefig("test_fig.png")
    

	


def get_data(path, start, end, bib) -> list:
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bibs WHERE bib_id = ? AND date BETWEEN ? AND ?",
        (bib, start, end)
    )
    #print(cur.fetchall())
    return cur.fetchall()


if __name__ == "__main__":
	#db_path = "/var/lib/bib-spaces-analyzer/spaces.db" if platform.startswith("linux") else "spaces.db"
	#db_path = input("path to database")
    db_path = "test.db"
    get_data(db_path, "2022-01-01 00:00:00", "2023-01-01 00:00:00", 1)
    plot_timeinterval("test.db", "2022-01-01 00:00:00", "2023-01-01 00:00:00", ["1", "2", "3"])