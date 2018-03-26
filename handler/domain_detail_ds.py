#!coding=utf8

import time
import io
import mysql
import utils

pds = []

def read_data():
	# 从文件中读取恶意域名信息
	with io.open("../data/3mths.txt", "r", encoding="latin1") as f:
		for line in f.readlines():
			temp = line.strip().split("=")
			temp[0] = temp[0].strip()
			# temp[1] = temp[1].split(",")
			pds.append(temp[0])

def create_db():
	sql = ("CREATE TABLE IF NOT EXISTS domain_detail ( domain_id INT(10) UNSIGNED NOT NULL DEFAULT 0," 
		"primary_domain VARCHAR(128) NOT NULL DEFAULT '', "
		"is_dga INT(10) UNSIGNED NOT NULL DEFAULT 0, "
     	"ttl INT(10) UNSIGNED NOT NULL DEFAULT 0, "
	    "registrar VARCHAR(64) DEFAULT '', "
	    "registrant VARCHAR(64) DEFAULT '', "
	    "register_length VARCHAR(16) DEFAULT '', "
	    "ip_active INT(10) UNSIGNED DEFAULT 0, "
	    "ip_port TEXT, "
	    "PRIMARY KEY(domain_id, primary_domain) "
	    " ) ENGINE=INNODB DEFAULT CHARSET=utf8;")

	try:
		mysql.cursor.execute(sql)
		mysql.conn.commit()
	except Exception as e:
		mysql.conn.rollback()
		raise e

def init_db():
	# 初始化对应的域名基本信息
	for item in pds:
		sql_name = ("INSERT INTO domain_detail (domain_id, primary_domain, is_dga, ttl) "
			"SELECT domain_id, primary_domain, is_dga, ttl FROM domain_name "
			"WHERE primary_domain = '%s';" % item)
		
		try:
			mysql.cursor.execute(sql_name)
			mysql.conn.commit()
		except Exception as e:
			mysql.conn.rollback()
			raise e

	# 初始化对应的whois信息
	sql_whois = ("UPDATE domain_detail as a INNER JOIN domain_whois as b "
		"on a.primary_domain=b.primary_domain SET "
		"a.registrar=b.registrar, a.registrant=b.registrant;")
	try:
		mysql.cursor.execute(sql_whois)
		mysql.conn.commit()
	except Exception as e:
		mysql.conn.rollback()
		raise e

def add_register_length():
	times = []
	time_diff = []

	for item in pds:
		sql_get = ("SELECT register_date, expire_date FROM domain_whois "
		"WHERE primary_domain = '%s';") % item

		mysql.cursor.execute(sql_get)
		rs = mysql.cursor.fetchone()

		if rs != None:
			times.append(list(rs))
		else:
			times.append([])

	for item in times:
		# if len(item) != 0:
		# 	if item[0] != '' and item[1] != '':
		try:	
			temp = utils.standard2timestamp(item[1]) - utils.standard2timestamp(item[0])
			time_diff.append(utils.timestamp2diff(temp))
		except:
			time_diff.append('')

	for i in range(0, len(pds)):
		sql_set = ("UPDATE domain_detail SET register_length = '%s' "
		"WHERE primary_domain = '%s';") % (time_diff[i], pds[i])

		try:
			mysql.cursor.execute(sql_set)
			mysql.conn.commit()
		except Exception as e:
			mysql.conn.rollback()
			raise e


if __name__ == "__main__":
	try:
		read_data()
		#create_db()
		#init_db()
		add_register_length()
	# except Exception as e:
	# 	print(e, time.asctime(time.localtime(time.time())))
	finally:
		mysql.conn.close()