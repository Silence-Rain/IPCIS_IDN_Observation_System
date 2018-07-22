#!coding=utf8

class DomainListModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	async def get_known_domains(self):
		ret = []
		rs = await self.ipcis.query(
			"SELECT domain_name FROM domain2ip;")
		for item in rs:
			ret.append(item[0])

		return ret