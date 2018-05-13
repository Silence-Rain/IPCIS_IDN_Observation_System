#!coding=utf8

class TopoModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	def formatter(raw_tup, label_list):
		ret = {}
		for index, label in enumerate(label_list):
			ret[label] = raw_tup[index]
		return ret

	async def get_ip(domain):
		ips = await self.db.ipcis.query(
			"SELECT ip_1 FROM domain2ip WHERE domain_name='%s';" % domain)
		return list(ips)

	async def get_ip_activities(ips):
		ret = []
		for ip in ips:
			rs = await self.ipcis.query(
				"SELECT ip_1,ip_2,count FROM ip_activity_record WHERE ip_1=%s" % ip)
			for item in rs:
				ret.append(item)

		return ret