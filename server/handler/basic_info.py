#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class BasicInfoHandler(BaseHandler):

	"""
		@api {post}	/info/basic  域名基本信息
		@apiGroup	info
		@apiVersion	1.0.0
		@apiDescription 获取域名解析IP基本信息（流记录库）
		@apiPermission all

		@apiParam	{String}	domain_name	要查询的域名
		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	域名解析IP基本信息

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"domain_name": "www.test.com",
				"lang": "瑞典语,
				"ip": [
					{
						"ip": "118.89.140.118",
						"location": "中国-上海-上海",
						"auth": "中国-教育网-上海交通大学"
					}
				]
			}
	"""

	async def post(self):
		domain = str(self.get_argument("domain_name"))
		res = await self.db.info.get_basic_info(domain)

		self.finish_success(result=res)

class WhoisInfoHandler(BaseHandler):

	"""
		@api {post}	/info/whois  域名whois信息
		@apiGroup	info
		@apiVersion	1.0.0
		@apiDescription 获取域名whois信息（IPCIS_DNS_DB库）
		@apiPermission all
		
		@apiParam	{String}	domain_name	要查询的域名
		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	域名whois信息

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
				"domain_name": "www.test.com",
				"whois": {
					"registrar": "注册人",
					"registrant": "注册机构",
					"address": "注册机构地址",
					"email": "test@email.com",
					"register_date": "17-jun-2005",
					"expire_date": "17-jun-2020"
				}
			}
	"""

	async def post(self):
		domain = str(self.get_argument("domain_name"))
		res = await self.db.info.get_whois_info(domain)

		self.finish_success(result=res)


routes.handlers += [
	(r'/info/basic', BasicInfoHandler),
	(r'/info/whois', WhoisInfoHandler)
]