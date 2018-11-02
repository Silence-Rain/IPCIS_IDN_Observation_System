#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class TransTopoHandler(BaseHandler):

	"""
		@api {post}	/topo  获取通信对端IP拓扑网络
		@apiGroup	topo
		@apiVersion	1.0.0
		@apiDescription 对指定域名，获取指定时间段内所有通信对端拓扑网络
		@apiPermission all

		@apiParam	{String}	ips		要查询的域名解析IP
		@apiParam	{Number}	length	要查询的天数
		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	所有通信对端的拓扑网络

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"nodes": [
					{
						"id": 0, 
						"name": "118.89.140.118"
					},
					{
						"id": 1, 
						"name": "211.65.193.23"
					},
					...
				], 
				"links": [
					{
						"source": 0, 
						"target": 1
					},
					...
				]
			}
	"""

	async def post(self):
		ips = self.get_argument("ips")
		length = self.get_argument("length")
		res = await self.db.topo.get_max_topo(ips, length)
		self.finish_success(result=res)


routes.handlers += [
	(r'/topo', TransTopoHandler)
]