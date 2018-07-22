#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class DomainListHandler(BaseHandler):

	"""
		@api {get}	/list  已知恶意域名
		@apiGroup	list
		@apiVersion	1.0.0
		@apiDescription 获取已知恶意域名列表
		@apiPermission all

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	已知恶意域名列表

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			[
			    "www.test.com",
			    "tieba.baidu.com"
			    ...
			]
	"""

	async def get(self):
		res = await self.db.list.get_known_domains()
		self.finish_success(result=res)


routes.handlers += [
	(r'/list', DomainListHandler)
]