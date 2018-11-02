#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class DomainListHandler(BaseHandler):

	"""
		@api {get}	/list  已知IDN列表
		@apiGroup	list
		@apiVersion	1.0.0
		@apiDescription 获取已知IDN列表，已知所有语种列表
		@apiPermission all

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	已知IDN列表

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"res": [
					{
						"domain_name": "www.中国慢病网.com", 
						"lang": "中文"
					},
					...
				], 
				"all_lang": ["瑞典语", "日语", ...]
			}
	"""

	async def get(self):
		res = await self.db.list.get_known_idns()
		res_lang = await self.db.list.get_all_langs()

		self.finish_success(result={"res": res, "all_lang": res_lang})


routes.handlers += [
	(r'/list', DomainListHandler)
]