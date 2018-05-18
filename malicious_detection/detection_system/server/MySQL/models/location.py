#!coding=utf8

class LocationModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	def formatter(self, raw):
		ret = {}
		temp = raw[2].split(",")
		ret["lng"] = float(temp[0])
		ret["lat"] = float(temp[1])
		ret["ip"] = raw[0]
		ret["location"] = raw[1]
		ret["count"] = eval(raw[3])

		return ret

	async def get_location(self, domain):
		rs = await self.ipcis.query(
			"SELECT ip_1,ip_1_location,ip_1_lnglat,ip_activity FROM domain2ip WHERE domain_name='%s';" % domain)
		ret = []
		for item in rs:
			ret.append(self.formatter(item))

		return ret
