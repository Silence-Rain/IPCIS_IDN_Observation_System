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

	async def add_idn(self, domain, val):
		ttl = val["ttl"] if "ttl" in val else None
		timestamp = val["timestamp"] if "timestamp" in val else None
		ip = val["ip"] if "ip" in val else None
		lang = val["lang"] if "lang" in val else None

		sql = "INSERT INTO known_idns VALUES (%s, %s)"