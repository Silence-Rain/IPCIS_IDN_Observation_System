import io
import asyncio
import sys
sys.path.append("../")
from config import *
from dao.mysql import MySQL

# 聚类相同域名的解析IP
def cluster(path):
	ret = []
	with io.open(path, "r", encoding="utf8") as f:
		idn_set = {}
		for line in f.readlines():
			temp = line.strip().split(",")
			if temp[0] in idn_set:
				if int(temp[1]) not in idn_set[temp[0]][0]:
					idn_set[temp[0]][0].append(int(temp[1]))
			else:
				idn_set[temp[0]] = [[int(temp[1])], temp[2]]
		for domain in idn_set:
			ret.append([domain, idn_set[domain][0], idn_set[domain][1]])
	return ret

async def insert(data):
	db = MySQL(
		host=DNS_HOST,
		user=DNS_USER,
		passwd=DNS_PASSWD,
		port=DNS_PORT,
		db=DNS_DB
	)

	try:
		for item in data:
			sql = "INSERT INTO known_idns (domain_name, ip, lang) VALUES ('%s', '%s', '%s')" % (item[0], str(item[1]), item[2])
			await db.execute(sql)
	except Exception as e:
		print(e)


if __name__ == '__main__':
	data = cluster("/Users/Silence/Desktop/minority.txt")

	loop = asyncio.get_event_loop()
	loop.run_until_complete(insert(data))
