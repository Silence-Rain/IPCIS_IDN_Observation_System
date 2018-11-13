import io
import requests
import random
from collections import Counter
import sys
sys.path.append("../")
from config import *

ret = []
with io.open("../data/res.dat", "r", encoding="utf8") as f:
	content = eval(f.readline())
	domain_set = {}
	for item in content:
		if item["domain"] not in domain_set:
			domain_set[item["domain"]] = item["ip"]

	for index, k in enumerate(list(domain_set.keys())[:20]):
		print(index)
		ip = domain_set[k]
		url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=1" % (ip, "2018-10-17")
		proxy = IPCIS_PROXY

		try:
			r = requests.get(url, proxies=proxy)
		except Exception as e:
			print(e)
			continue

		res = r.json()[ip+":32"]
		item = res[1]

		if len(item) == 0:
			continue

		# 从一天的流记录中取10条，取10条记录中出现次数最多的端口为其代表端口
		port = []
		if len(item) <= 11:
			for i in item[1:]:
				port.append(i.split(" ")[15])
		else:
			records = item[1:]
			random.shuffle(records)
			for i in records[1:11]:
				port.append(i.split(" ")[15])

		port_counts = Counter(port)
		top_port = port_counts.most_common(1)[0][0]
		ret.append([k, top_port])

with io.open("./result.csv", "w", encoding="utf8") as f:
	for item in ret:
		f.write(item[0] + "," + item[1] + "\n")

