#!coding=utf8

class InfoModel(object):
	def __init__(self, ipcis, dns):
		self.ipcis = ipcis
		self.dns = dns

	def formatter(self, raw_tup, label_list):
		ret = {}
		for index, label in enumerate(label_list):
			ret[label] = raw_tup[index]
		return ret

	async def get_primary_domain(self, domain):
		ret = await self.db.ipcis.get(
			"SELECT primary_domain FROM primary2name WHERE domain_name='%s';" % domain)

		if len(ret) != 0:
			return ret[0]
		else:
			return None

	async def get_info(self, domain, pd):
		rs_static = await self.ipcis.get(
			"SELECT is_dga,ttl,credit FROM domain_static WHERE primary_domain='%s';" % pd)
		rs_whois = await self.dns.get(
			"SELECT registrar,registrant,address,email,register_date,expire_date FROM domain_whois WHERE primary_domain='%s';" % pd)
		rs_ip = await self.ipcis.query(
			"SELECT ip_1,ip_location,ip_activity FROM domain2ip WHERE domain_name='%s'" % domain)

		ret = {}
		ret["domain_name"] = domain
		ret["static"] = self.formatter(rs_static, ["is_dga","ttl","credit"])
		ret["whois"] = self.formatter(rs_whois, ["registrar","registrant","address","email","register_date","expire_date"])
		ret["ip"] = self.formatter(list(rs_ip), ["ip","location","count"])

		return ret