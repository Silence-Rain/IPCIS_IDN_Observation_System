#!coding=utf8

class ServiceModel(object):
	def __init__(self, ipcis):
		self.ipcis = ipcis

	async def get_raw_data(self, domain):
		return {}
