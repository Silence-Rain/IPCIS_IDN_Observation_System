#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.graph import *

class TopoSteadyHandler(BaseHandler):

	async def get(self):
		domain = self.get_argument("domain_name")
		ips = await self.db.topo.get_ip(domain)
		acts = await self.db.topo.get_ip_activities(ips)
		res = steady_topo(acts)
		self.finish_success(result=res)

class TopoMaxHandler(BaseHandler):

	async def get(self):
		domain = self.get_argument("domain_name")
		ips = await self.db.topo.get_ip(domain)
		acts = await self.db.topo.get_ip_activities(ips)
		res = max_topo(acts)	
		self.finish_success(result=res)


routes.handlers += [
	(r'/topo/steady', TopoSteadyHandler),
	(r'/topo/max', TopoMaxHandler)
]