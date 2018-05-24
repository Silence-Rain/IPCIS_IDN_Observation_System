#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class InfoIPCISHandler(BaseHandler):

	async def post(self):
		domain = str(self.get_argument("domain_name"))
		pd = await self.db.info.get_primary_domain(domain)
		res = await self.db.info.get_ipcis_info(domain, pd)

		self.finish_success(result=res)

class InfoDNSHandler(BaseHandler):

	async def post(self):
		domain = str(self.get_argument("domain_name"))
		pd = await self.db.info.get_primary_domain(domain)
		res = await self.db.info.get_dns_info(domain, pd)

		self.finish_success(result=res)


routes.handlers += [
	(r'/info/local', InfoIPCISHandler),
	(r'/info/remote', InfoDNSHandler)
]