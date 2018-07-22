#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class LocationHandler(BaseHandler):

	"""
		@api {get}	/location  解析IP地理位置
		@apiGroup	location
		@apiVersion	1.0.0
		@apiDescription 获取域名解析IP的地理位置与经纬度坐标
		@apiPermission all
		@apiParam	{String}	domain_name	要查询的域名

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	域名解析IP地理位置信息

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			[
			    {
			        "lng": 118.8028, 
			        "lat": 32.0647,
			        "ip": "202.112.23.167",
			        "location": "中国-江苏-南京",
			        "count": [25,50...]
			    }
			    ...
			]
	"""

	async def get(self):
		domain = self.get_argument("domain_name")
		res = await self.db.location.get_location(domain)
		self.finish_success(result=res)


routes.handlers += [
	(r'/location', LocationHandler)
]