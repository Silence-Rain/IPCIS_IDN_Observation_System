#!coding=utf8

import mysql
import time

def create_db():
	sql = ("CREATE TABLE IF NOT EXISTS domain_detail ( domain_id INT(10) UNSIGNED NOT NULL DEFAULT 0," 
		"primary_domain VARCHAR(128) NOT NULL DEFAULT '', "
		"is_dga INT(10) UNSIGNED NOT NULL DEFAULT 0, "
     	"ttl INT(10) UNSIGNED NOT NULL DEFAULT 0, "
	    "registrar VARCHAR(64), "
	    "registrant VARCHAR(64), "
	    "register_date VARCHAR(16), "
	    "expire_date VARCHAR(16), "
	    "PRIMARY KEY(domain_id, primary_domain) "
	    " ) ENGINE=INNODB DEFAULT CHARSET=utf8;")

	try:
		mysql.cursor.execute(sql)
		mysql.conn.commit()
	except Exception as e:
		mysql.conn.rollback()
		raise e

def init_db():
	# 对domain_name和domain_whois表中的信息进行初始化
	sql_name = ("INSERT INTO domain_detail (domain_id, primary_domain, is_dga, ttl) "
		"SELECT domain_id, primary_domain, is_dga, ttl FROM domain_name;")
	sql_whois = ("UPDATE domain_detail as a INNER JOIN domain_whois as b "
		"on a.primary_domain=b.primary_domain SET "
		"a.registrar=b.registrar, a.registrant=b.registrant, "
		"a.register_date=b.register_date, a.expire_date=b.expire_date;")
	try:
		mysql.cursor.execute(sql_name)
		mysql.cursor.execute(sql_whois)
		mysql.conn.commit()
	except Exception as e:
		mysql.conn.rollback()
		raise e

	# 对resolved_ip表中的信息进行初始化
	# sql_select_id = "SELECT domain_id FROM domain_detail;"
	# mysql.cursor.execute(sql_select_id)
	# rs_id = mysql.cursor.fetchall()

	# for item in rs_id:
	# 	sql_select_ip = "SELECT DISTINCT ip FROM resolved_ip WHERE domain_id=%s;" % (item[0])
	# 	mysql.cursor.execute(sql_select_ip)
	# 	rs_ip = mysql.cursor.fetchall()
	# 	ret = ""

	# 	if len(rs_ip) >= 10000:
	# 		rs_ip = rs_ip[:10000]

	# 	for ip in rs_ip:
	# 		ret += "%d," % (ip[0])
	# 	ret = ret[:-1]

	# 	sql_ip = "UPDATE domain_detail SET ips='%s' WHERE domain_id=%s;" % (ret, item[0])
	# 	try:
	# 		mysql.cursor.execute(sql_ip)
	# 		mysql.conn.commit()
	# 	except Exception as e:
	# 		mysql.conn.rollback()
	# 		raise e


if __name__ == "__main__":
	try:
		create_db()
		init_db()
		print("complete!")
	except Exception as e:
		print(e, time.asctime(time.localtime(time.time())))
	finally:
		mysql.conn.close()