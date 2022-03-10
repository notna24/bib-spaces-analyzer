#!/usr/bin/python3

import requests as req
from requests.exceptions import ConnectionError
import time
import sqlite3
import logging
#   this script gets the available seats in the libraries of TU Berlin
#   it fetches the data from their Website
#   I want to plot it in the

URL = "https://services.ub.tu-berlin.de/platzbuchung/locations/spaces"


class Robot:
	def __init__(self, url : str, id : int, interval : int, db_path : str):
		self.id = id
		self.url = url
		self.interval = interval # time the robot sleeps between calls in seconds
		self.status = True
		self.db_path = db_path
		#self.db_handle = sqlite3.connect(db_path)
		logging.basicConfig(filename=f"robot_{self.id}.log", encoding="utf-8", level=logging.INFO)


	def run(self):
		while self.status:
			data = self.fetch_seats()
			if data is not False:
				self.store_data(data)
			# maybe switch to a specific time based system
			time.sleep(self.interval) # 5 min

	def store_data(self, data):
		with sqlite3.connect(self.db_path) as con:
			local_time = time.localtime(time.time()) # timestamp
			cur = con.cursor()
			for id, info in data.items():
				cur.execute("insert into bibs values (?, ?, ?, ?)", (
					time.strftime('%Y-%m-%d %H:%M:%S'),
					id,
					info.get("free_spaces"),
					info.get("is_currently_open")
				)) # doing it securely
			con.commit()

	def fetch_seats(self) -> dict or bool:
		try:
			resp = req.get(self.url)
		except ConnectionError as E:
			logging.exception(E)
			return False
		if resp.status_code != 200:
			logging.error(f"wrong response status:{resp.status_code}:{resp.text}") # might be vulnerable, if there is a zero day rce in the logging lib ;)
			return False
		return resp.json()

def init_db(path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE bibs (date DATETIME, bib_id, free_seats, status)''')
        con.commit()


if __name__ == "__main__":
	import configparser
	from sys import platform
	import os

	config = configparser.ConfigParser()
	config.read("robot.conf")
	url = config.get("DEFAULT", "url")
	db_dir = config.get("DATABASE", "DBParentDir")
	db_name = config.get("DATABASE", "DBName")
	interval = config.get("DEFAULT", "interval")

	if os.path.isdir(db_dir) is False:
		print(f"Database path not found. Creating folder {db_dir}")
		os.makedirs(db_dir)

	if os.path.isfile(db_dir + db_name) is False:
		print("Database File was not found. Creating new Database!")
		init_db(db_dir + db_name)

	print("seat fetching started")

	robot = Robot(url, 0, 300, db_dir + db_name)
	print(robot.run())
