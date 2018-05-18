from .models.info import InfoModel
from .models.topo import TopoModel
from .models.location import LocationModel
from .models.active import ActiveModel
from .models.service import ServiceModel

class Database(object):
	def __init__(self, ipcis, dns):
		self.ipcis = ipcis
		self.dns = dns

		self.info = InfoModel(self.ipcis, self.dns)
		self.topo = TopoModel(self.ipcis)
		self.location = LocationModel(self.ipcis)
		self.active = ActiveModel(self.ipcis)
		self.service = ServiceModel(self.ipcis)