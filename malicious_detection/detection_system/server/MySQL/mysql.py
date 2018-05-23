#!coding=utf8

import pymysql
import time
import sched

class MySQL(object):
	def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
		self.port = port
		self.charset = charset
		self.connect()

	async def get(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchone()

	async def query(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	async def execute(self, sql):
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()

	def connect(self):
		self.conn = pymysql.connect(
						host = self.host, 
						port = self.port, 
						user = self.user,
						passwd = self.passwd,
						db = self.db,
						charset = self.charset
						)
		self.cursor = self.conn.cursor()

	def refresh(self):
		self.close()
		s = sched.scheduler(time.time, time.sleep)
		s.enter(28000, self.connect)
		s.run()

	def close(self):
		self.cursor.close()
		self.conn.close()