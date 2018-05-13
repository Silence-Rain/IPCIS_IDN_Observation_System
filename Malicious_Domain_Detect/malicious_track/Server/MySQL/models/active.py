#!coding=utf8

class ActiveModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	async def get_ip_and_count(domain):
		rs = await self.db.ipcis.query(
			"SELECT ip_1,ip_activity FROM domain2ip WHERE domain_name='%s';" % domain)
		return list(rs)

	async def get_raw_data(ips):
		ret = []
		for ip in ips:
			temp = {"ip": ip[0], "count": ip[1]}

			rs = await self.db.ipcis.query(
				"SELECT count(*),ip_2_location FROM ip_activity_record WHERE ip_1=%s;" % ip[0])
			for item in rs:
				temp["opposite_ip_count"] = item[0]
				temp["ip_geo"] = item[1]
			ret.append(temp)

		return ret
