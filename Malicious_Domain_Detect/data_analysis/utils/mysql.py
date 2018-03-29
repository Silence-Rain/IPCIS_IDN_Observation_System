#coding: utf8

import pymysql

conn = pymysql.connect(
			host = 'localhost', 
			port = 3307, 
			user = 'SQLadmin',
			passwd = 'adminofmysql',
			db = 'IPCIS_DB',
			charset = 'utf8'
			)
cursor = conn.cursor()