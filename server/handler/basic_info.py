#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes

class BasicInfoHandler(BaseHandler):

	"""
		@api {post}	/info/local  域名基本信息
		@apiGroup	info
		@apiVersion	1.0.0
		@apiDescription 获取域名基本信息和IP活动记录（known_malicious库）
		@apiPermission all
		@apiParam	{String}	domain_name	要查询的域名

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	域名的基本信息和IP活动记录

		@apiSuccessExample {json} 正常响应:
			HTTP/1.1 200 OK
			{
			    "domain_name": "www.test.com",
			    "static": {
			        "is_dga": 0,
			        "ttl": 86400,
			        "credit": 70,
			    },
			    "ip": [
			        {
			            "ip": "118.89.140.118",
			            "location": "中国-上海-上海",
			            "dns": "8.8.8.8"
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
		@api {post}	/info/remote  域名whois信息
		@apiGroup	info
		@apiVersion	1.0.0
		@apiDescription 获取域名whois信息（IPCIS_DNS_DB库）
		@apiPermission all
		@apiParam	{String}	domain_name	要查询的域名

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{JSON}		result	域名的whois信息

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