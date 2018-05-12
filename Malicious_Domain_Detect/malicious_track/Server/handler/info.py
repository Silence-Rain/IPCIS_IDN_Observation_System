#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
from utils.enrich import *

class InfoHandler(BaseHandler):

	def formatter(raw_tup, label_list):
		ret = {}
		for index, label in enumerate(label_list):
			ret[label] = raw_tup[index]
		return ret

	async def post(self):
		domain = self.get_argument("domain_name")
		pd = await self.ipcis_db.get(
			"SELECT primary_domain FROM primary2name WHERE domain_name='%s';" % domain)
		rs_static = await self.ipcis_db.get(
			"SELECT is_dga,ttl,credit FROM domain_static WHERE primary_domain='%s';" % pd)
		rs_whois = await self.dns_db.get(
			"SELECT registrar,registrant,address,email,register_date,expire_date FROM domain_whois WHERE primary_domain='%s';" % pd)
		rs_ip = await self.ipcis_db.query(
			"SELECT ip_1,ip_location,ip_activity FROM domain2ip WHERE domain_name='%s'" % domain)

		ret = {}
		ret["domain_name"] = domain
		ret["static"] = formatter(rs_static, ["is_dga","ttl","credit"])
		ret["whois"] = formatter(rs_whois, ["registrar","registrant","address","email","register_date","expire_date"])
		ret["ip"] = formatter(list(rs_ip), ["ip","location","count"])

		self.finish_success(result=ret)

routes.handlers += [
    (r'/info', InfoHandler)
]