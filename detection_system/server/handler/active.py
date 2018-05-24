#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.active import *

class ActiveHandler(BaseHandler):

	"""
		@api {get}	/active  域名解析IP活跃度
		@apiGroup	active
		@apiVersion	1.0.0
		@apiDescription 获取域名的活跃度以及活跃度的历史测度（14天）
		@apiPermission all
		@apiParam	{String}	domain_name	要查询的域名

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	域名解析IP的活跃度和历史测度

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			[
			    {
				    "ip": "118.89.140.118",
				    "active": 90,
				    "count": [100,120,80,70...],
				    "opposite_ip_count": [10,15,8,9...],
				    "ip_geo_entropy": [1.12,2.34,0.86,4.77...]
			    }
				...
			]
	"""

	async def get(self):
		domain = self.get_argument("domain_name")
		ips = await self.db.active.get_ip_and_count(domain)
		raw = await self.db.active.get_raw_data(ips)
		res = active_degree(raw)
		self.finish_success(result=res)


routes.handlers += [
	(r'/active', ActiveHandler)
]