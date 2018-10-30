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
		ret["lang"] = rs[3]
		ret["ip"] = []

		for item in eval(rs[2]):
			ret["ip"].append({"ip": str(IP(item))})

		return ret

	async def get_whois_info(self, domain):
		rs_whois = await self.db.get(
			"SELECT registrar,registrant,address,email,register_date,expire_date FROM domain_whois WHERE primary_domain='%s';" % pd)
		ret = {}
		ret["domain_name"] = domain
		ret["whois"] = self.basic_formatter(rs_whois, ["registrar","registrant","address","email","register_date","expire_date"])

		return ret
