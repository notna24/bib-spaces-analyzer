#!/usr/bin/python3

import configparser
import sqlite3
from numpy import average
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sys import platform

def find_day_average(path, day, bib, freq="30min"):
    # day should not include time, only date
    # the sql selection works
    start = pd.to_datetime(day)
    end = start + pd.DateOffset(1)
    dates = pd.date_range(start, end, freq=freq)
    averages = {}
    for i, date in enumerate(dates):
        with sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            print(bib, date, dates[i + 1])
            cur.execute("SELECT free_seats FROM bibs WHERE bib_id = ? AND date BETWEEN ? AND ?",
            (bib, str(date), str(dates[i + 1]))
            )
            data = cur.fetchall()
        print(data)
        if len(data) != 0:
            averages[date] = sum(data)/len(data)
        else:
            pass
    return averages



def plot_timeinterval(path, start, end, bibs):
    #this function plots the spaces in a certain time interval
    data = {}
    for bib in bibs:
        raw_data = get_data(path, start, end, bib)
        data[bib] = ([i[0] for i in raw_data], [i[2] for i in raw_data])
    fig, ax = plt.subplots()
    for bib, t_s in data.items():
        ax.plot(t_s[0], t_s[1], label=bib)
    ax.xaxis.set_major_locator(mdates.DayLocator((1,15)))
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.legend()
    plt.show()


def get_data(path, start, end, bib) -> list:
    with sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bibs WHERE bib_id = ? AND date BETWEEN ? AND ?",
        (bib, start, end)
    )
    #print(cur.fetchall())
    return cur.fetchall()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("robot.conf")
    db_dir = config.get("DATABASE", "DBParentDir")
    db_name = config.get("DATABASE", "DBName")
    db_path = db_dir + db_name
    #get_data(db_path, "2022-01-01 00:00:00", "2023-01-01 00:00:00", 1)
    #plot_timeinterval(db_path, "2022-01-01 00:00:00", "2023-01-01 00:00:00", ["1", "2", "3", "4", "5"])
    find_day_average(db_path, "2022-02-25", "1")