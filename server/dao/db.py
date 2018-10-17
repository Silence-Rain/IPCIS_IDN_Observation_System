from .models.idn_list import IDNListModel
from .models.geo_distribution import GeoDistributionModel
from .models.basic_info import BasicInfoModel

class Database(object):
	def __init__(self, db):
		self.db = db

		self.list = IDNListModel(self.db)
		self.geo = GeoDistributionModel()
		self.info = BasicInfoModel(self.db)