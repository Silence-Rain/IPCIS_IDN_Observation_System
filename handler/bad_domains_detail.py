#!coding=utf8

import mysql
import io

res = []
res_whois = []
res_ttl = []

def read_data():
	with io.open("../data/3mths.txt", "r", encoding="utf8") as f:
		for line in f.readlines():
			temp = line.strip().split("=")
			temp[0] = temp[0].strip()
			temp[1] = temp[1].split(",")

			res.append(temp)

def get_whois():
	with io.open("../data/3mths_whois.txt", "w") as f:
		for item in res:
			sql = "select * from domain_whois where primary_domain='%s';" % item[0]
			mysql.cursor.execute(sql)
			rs = mysql.cursor.fetchone()

			if rs is None:
				pass
			else:
				res_whois.append(rs)

		for item in res_whois:
			f.write(str(item) + "\n")

def get_ttl():
	with io.open("../data/3mths_ttl.txt", "w") as f:
		for item in res:
			sql = "select primary_domain,is_dga,ttl from domain_name where primary_domain='%s';" % item[0]
			mysql.cursor.execute(sql)
			rs = mysql.cursor.fetchone()

			if rs is None:
				pass
			else:
				res_ttl.append(rs)

		for item in res_ttl:
			f.write(str(item) + "\n")

if __name__ == "__main__":
	read_data()
	# get_whois()
	get_ttl()