#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class DomainListHandler(BaseHandler):

	async def get(self):
		res = await self.db.list.get_known_domains()
		self.finish_success(result=res)


routes.handlers += [
	(r'/list', DomainListHandler)
]