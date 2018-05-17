#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.enrich import *

class InfoHandler(BaseHandler):

	async def post(self):
		domain = str(self.get_argument("domain_name"))
		pd = await self.db.info.get_primary_domain(domain)

		# 表中已有记录
		if not pd:
			res = await self.db.info.get_info(domain, pd)
			self.finish_success(result=res)
		else:
			if await enrich_info(domain):
				res = await self.db.info.get_info(domain, pd)
				self.finish_success(result=res)

routes.handlers += [
	(r'/info', InfoHandler)
]