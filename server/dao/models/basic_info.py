#!coding=utf8

import requests
from IPy import *

class BasicInfoModel(object):
	def __init__(self, db):
		self.db = db

	# whois信息的格式化
	def basic_formatter(self, raw, labels):
		ret = {}
		for index, label in enumerate(labels):
			if raw != None:
				ret[label] = raw[index]
			else:
				ret[label] = "-"

		return ret

	# 从流记录库中获取解析IP的归属信息和地理信息
	async def get_basic_info(self, domain):
		ret = {}
		rs = await self.db.get(
			"SELECT * FROM known_idns WHERE domain_name='%s';" % domain)
		
		ret["domain_name"] = domain
		ret["lang"] = rs[3]
		ret["ip"] = []

		# 取最近一天的流记录
		proxy = {"http": "http://yunyang:yangyun123@202.112.23.167:8080"}
		url_tables = "http://211.65.197.210:8080/IPCIS/activityDatabase/?Mode=3"
		r_tables = requests.get(url_tables, proxies=proxy)
		tables = r_tables.json()["tables"]
		date = tables[-1]

		for i in eval(rs[2]):
			ip_str = str(IP(i))
			url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=1" % (ip_str, date)
			r = requests.get(url, proxies=proxy)
			try:
				res = r.json()[ip_str+":32"]
			except Exception as e:
				print(e)
				ret["ip"].append({"ip": ip_str, "location": "暂无结果", "auth": "暂无结果"})

			# 获得解析IP归属和地址
			if len(res[0]) == 0:
				if len(res[1]) == 0:
					ret["ip"].append({"ip": ip_str, "location": "暂无结果", "auth": "暂无结果"})
				else:
					target_pos = res[1][0].split("$")[-2:]
					ret["ip"].append({"ip": ip_str, "location": target_pos[0], "auth": target_pos[1]})
			else:
				target_pos = res[0][0].split("$")[-2:]
				ret["ip"].append({"ip": ip_str, "location": target_pos[0], "auth": target_pos[1]})
			
		return ret

	# 从DNS库中获取whois信息
	async def get_whois_info(self, domain):
		# 根据已知的顶级域名后缀，求全域名的主域名
		suffixes = []
		with open("data/Internet_Domains_Suffixes") as f:
			for line in f.readlines():
				suffixes.append(line.strip().lower()[1:])
		labels = domain.split(".")
		labels.reverse()
		pds = []
		for item in labels:
			pds.append(item)
			if item not in suffixes:
				break
		pds.reverse()
		pd = ".".join(pds)

		try:
			rs_whois = await self.db.get(
				"SELECT registrar,registrant,address,email,register_date,expire_date FROM domain_whois WHERE primary_domain='%s';" % pd)
		except:
			rs_whois = None
		ret = {}
		ret["domain_name"] = domain
		ret["whois"] = self.basic_formatter(rs_whois, ["registrar","registrant","address","email","register_date","expire_date"])

		return ret

