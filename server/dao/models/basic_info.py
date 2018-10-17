#!coding=utf8

from IPy import *

class BasicInfoModel(object):
	def __init__(self, db):
		self.db = db

	def basic_formatter(self, raw, labels):
		ret = {}
		for index, label in enumerate(labels):
			ret[label] = raw[index]

		return ret

	async def get_basic_info(self, domain):
		ret = {}
		rs = await self.db.get(
			"SELECT * FROM known_idns WHERE domain_name='%s';" % domain)
		
		ret["domain_name"] = domain
		ret["ttl"] = rs[2] or "-"
		ret["timestamp"] = rs[3] or "-"
		ret["lang"] = rs[5]
		ret["ip"] = []

		for item in eval(rs[4]):
			ret["ip"].append({"ip": str(IP(item))})

		return ret

	async def get_whois_info(self, domain):
		rs_whois = await self.db.get(
			"SELECT registrar,registrant,address,email,register_date,expire_date FROM domain_whois WHERE primary_domain='%s';" % pd)
		ret = {}
		ret["domain_name"] = domain
		ret["whois"] = self.basic_formatter(rs_whois, ["registrar","registrant","address","email","register_date","expire_date"])

		return ret


	

	# def ip_formatter(self, raw):
	# 	ret = []
	# 	for item in raw:
	# 		temp = {"ip":"", "location":"", "dns":""}
	# 		temp["ip"] = str(IP(item[0]))
	# 		temp["location"] = item[1]
	# 		temp["dns"] = item[2]
	# 		ret.append(temp)

	# 	return ret

	# async def get_primary_domain(self, domain):
	# 	ret = await self.db.get(
	# 		"SELECT primary_domain FROM primary2name WHERE domain_name='%s';" % domain)

	# 	if ret != None:
	# 		return ret[0]
	# 	else:
	# 		return None

	# async def get_dns_info(self, domain, pd):
	# 	rs_whois = await self.db.get(
	# 		"SELECT registrar,registrant,address,email,register_date,expire_date FROM domain_whois WHERE primary_domain='%s';" % pd)
	# 	ret = {}
	# 	ret["domain_name"] = domain
	# 	ret["whois"] = self.basic_formatter(rs_whois, ["registrar","registrant","address","email","register_date","expire_date"])

	# 	return ret

	# async def get_ipcis_info(self, domain, pd):
	# 	rs_static = await self.db.get(
	# 		"SELECT is_dga,ttl,credit FROM domain_static WHERE primary_domain='%s';" % pd)	
	# 	rs_ip = await self.db.query(
	# 		"SELECT ip_1,ip_1_location,dns FROM domain2ip WHERE domain_name='%s';" % domain)
	# 	ret = {}
	# 	ret["domain_name"] = domain
	# 	ret["static"] = self.basic_formatter(rs_static, ["is_dga","ttl","credit"])
	# 	ret["ip"] = self.ip_formatter(rs_ip)

	# return ret