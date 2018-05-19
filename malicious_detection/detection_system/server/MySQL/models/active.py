#!coding=utf8

class ActiveModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	async def get_ip_and_count(self, domain):
		ret = []
		rs = await self.ipcis.query(
			"SELECT ip_1,ip_activity FROM domain2ip WHERE domain_name='%s';" % domain)
		for item in rs:
			ret.append([item[0], eval(item[1])])

		return ret

	async def get_raw_data(self, ips):
		ret = []
		for ip in ips:
			temp = {"ip": ip[0], "count": ip[1], "opposite_ip": {}, "ip_geo": {}}

			rs = await self.ipcis.query(
				"SELECT ip_2,ip_2_lnglat,date FROM ip_activity_record WHERE ip_1=%s;" % ip[0])
			for item in rs:
				if item[2] not in temp["opposite_ip"]:
					temp["opposite_ip"][item[2]] = [item[0]]
					temp["ip_geo"][item[2]] = [item[1]]
				else:
					temp["opposite_ip"][item[2]].append(item[0])
					temp["ip_geo"][item[2]].append(item[1])
			ret.append(temp)

		return ret
