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
		res = await self.db.list.get_known_idns()
		
		# 统计所有语种，出现次数小于5次的统一归为“其他语种”
		lang_set = []
		all_lang_raw = []
		for item in res:
			if item["lang"] not in lang_set:
				lang_set.append(item["lang"])
				all_lang_raw.append({"value": item["lang"], "label": item["lang"], "count": 1})
			else:
				all_lang_raw[lang_set.index(item["lang"])]["count"] += 1
		all_lang = []
		for item in all_lang_raw:
			if item["count"] > 1:
				all_lang.append(item)
		all_lang.append({"value": "其他语种", "label": "其他语种"})

		self.finish_success(result={"res": res, "all_lang": all_lang})

	async def put(self):
		domain = self.get_argument("domain")
		val = self.get_argument("val")


routes.handlers += [
	(r'/list', DomainListHandler)
]