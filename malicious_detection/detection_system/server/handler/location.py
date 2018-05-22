#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class LocationHandler(BaseHandler):

	async def get(self):
		domain = self.get_argument("domain_name")
		res = await self.db.location.get_location(domain)
		self.finish_success(result=res)


routes.handlers += [
	(r'/location', LocationHandler)
]