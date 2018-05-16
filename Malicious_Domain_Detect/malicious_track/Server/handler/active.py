#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.active import *

class ActiveHandler(BaseHandler):

	async def get(self):
		domain = self.request.headers["domain_name"]
		ips = self.db.active.get_ip_and_count(domain)
		raw = self.db.active.get_raw_data(ips)
		res = active_degree(raw)

		self.finish_success(result=res)


routes.handlers += [
	(r'/active', ActiveHandler)
]