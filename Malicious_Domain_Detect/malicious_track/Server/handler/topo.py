#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.graph import *

class TopoSteadyHandler(BaseHandler):

	async def get(self):
		domain = self.request.headers["domain_name"]
		ips = self.db.topo.get_ip(domain)
		acts = self.db.topo.get_ip_activities(ips)
		res = steady_topo(acts)

		self.finish_success(result=res)

class TopoMaxHandler(BaseHandler):

	async def get(self):
		domain = self.request.headers["domain_name"]
		ips = self.db.topo.get_ip(domain)
		acts = self.db.topo.get_ip_activities(ips)
		res = max_topo(acts)
		
		self.finish_success(result=res)

routes.handlers += [
	(r'/topo/steady', TopoSteadyHandler),
	(r'/topo/max', TopoMaxHandler)
]