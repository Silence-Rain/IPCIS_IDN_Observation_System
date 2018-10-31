#!coding=utf8

class IDNListModel(object):
	def __init__(self, db):
		self.db = db

	async def get_known_idns(self):
		ret = []
		rs = await self.db.query("SELECT domain_name, lang FROM known_idns;")
		for item in rs:
			ret.append({"domain_name": item[0], "lang": item[1]})

		return ret

	async def get_all_langs(self):
		ret = []
		try:
			rs = await self.db.query("SELECT DISTINCT(lang) FROM known_idns;")
		except:
			rs = []
		for item in rs:
			ret.append(item[0])

		return ret