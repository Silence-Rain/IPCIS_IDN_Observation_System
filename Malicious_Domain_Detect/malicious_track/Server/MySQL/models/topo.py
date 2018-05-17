#!coding=utf8

class TopoModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	async def get_ip(self, domain):
		ret = []
		ips = await self.db.ipcis.query(
			"SELECT ip_1 FROM domain2ip WHERE domain_name='%s';" % domain)
		for ip in ips:
			ret.append(ip[0])

		return ret

	async def get_ip_activities(self, ips):
		ret = []
		for ip in ips:
			rs = await self.ipcis.query(
				"SELECT ip_1,ip_2,count FROM ip_activity_record WHERE ip_1=%s" % ip)
			for item in rs:
				ret.append(list(item))

		return ret