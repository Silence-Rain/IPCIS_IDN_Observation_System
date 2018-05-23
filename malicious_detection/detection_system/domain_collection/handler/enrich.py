#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from handler.auto import *

class EnrichHandler(BaseHandler):

	async def post(self):
		domain = str(self.get_argument("domain_name"))
		res = await newip(domain)

		self.finish_success(result=res)


routes.handlers += [
	(r'/enrich', EnrichHandler)
]