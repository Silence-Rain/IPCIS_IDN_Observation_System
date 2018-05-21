#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.service import *

class ServiceHandler(BaseHandler):

	async def get(self):
		domain = self.request.headers["domain_name"]
		raw = await self.db.service.get_raw_data(domain)
		res = service_type(raw)
		self.finish_success(result=res)


routes.handlers += [
	(r'/service', ServiceHandler)
]