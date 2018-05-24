#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.topo import *

class TopoSteadyHandler(BaseHandler):

	"""
		@api {get}	/topo/steady  通信活动稳定拓扑
		@apiGroup	topo
		@apiVersion	1.0.0
		@apiDescription 获取域名解析IP通信活动的稳定拓扑结构
		@apiPermission all
		@apiParam	{String}	domain_name	要查询的域名

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	稳定拓扑结构的图数据

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
			    "nodes": [
			        {
			            "id": 0,
			            "name": "118.89.140.118",
			            "count": 100
			        },
			        {
			            "id": 1,
			            "name": "45.77.86.38",
			            "count": 50
			        }
			        ...
			    ],
			    "links": [
			        {
			            "source": 0,
			            "target": 1
			        },
			        {
			            "source": 1,
			            "target": 2
			        },
			        ...
			    ]
			}
	"""

	async def get(self):
		domain = self.get_argument("domain_name")
		ips = await self.db.topo.get_ip(domain)
		acts = await self.db.topo.get_ip_activities(ips)
		res = steady_topo(acts)
		self.finish_success(result=res)

class TopoMaxHandler(BaseHandler):

	"""
		@api {get}	/topo/max  通信活动最大拓扑
		@apiGroup	topo
		@apiVersion	1.0.0
		@apiDescription 获取域名解析IP通信活动的最大拓扑结构
		@apiPermission all
		@apiParam	{String}	domain_name	要查询的域名

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	最大拓扑结构的图数据

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"nodes": [
					{
						"id": 0,
						"name": "118.89.140.118",
						"count": 100
					},
					{
						"id": 1,
						"name": "45.77.86.38",
						"count": 50
					}
					...
				],
				"links": [
					{
						"source": 0,
						"target": 1
					},
					{
						"source": 1,
						"target": 2
					},
					...
				]
			}
	"""

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