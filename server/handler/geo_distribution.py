#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class GeoDistributionHandler(BaseHandler):

	"""
		@api {post}	/location  获取通信对端IP地理信息
		@apiGroup	location
		@apiVersion	1.0.0
		@apiDescription 对指定域名，获取指定时间段内所有通信对端地理位置与归属信息
		@apiPermission all

		@apiParam	{String}	ips		要查询的域名解析IP
		@apiParam	{Number}	length	要查询的天数
		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	所有通信对端地理位置与归属信息

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"self": [
					{
						"ip": "118.89.140.118",
						"location": "中国-上海-上海",
						"auth": "中国-教育网-上海交通大学",
						"lng": 118.90,
						"lat": 32.43
					},
					...
				]
			}
	"""

	async def post(self):
		ips = self.get_argument("ips")
		length = self.get_argument("length")
		res = await self.db.geo.get_geo_distribution(ips, length)
		self.finish_success(result=res)


class GeoDistributionAllHandler(BaseHandler):

	"""
		@api {get}	/location_all  获取所有IDN解析IP地理信息
		@apiGroup	location
		@apiVersion	1.0.0
		@apiDescription 获取指定语种的所有IDN解析IP地理信息
		@apiPermission all

		@apiParam	{String}	lang	要查询的语种
		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	所有解析IP地理位置与归属信息

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"self": [
					{
						"ip": "118.89.140.118",
						"location": "中国-上海-上海",
						"auth": "中国-教育网-上海交通大学",
						"lng": 118.90,
						"lat": 32.43
					}
				], 
				"opposite": [
					{
						"ip": "211.65.193.23",
						"location": "中国-江苏-南京",
						"auth": "中国-教育网-东南大学",
						"lng": 112.87,
						"lat": 31.66
					},
					...
				]
			}
	"""

	async def post(self):
		lang = self.get_argument("lang")
		res = await self.db.geo.get_all_geo_distribution(lang)
		self.finish_success(result=res)


routes.handlers += [
	(r'/location', GeoDistributionHandler),
	(r'/location_all', GeoDistributionAllHandler)
]