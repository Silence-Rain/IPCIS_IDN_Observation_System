#!coding=utf8

from tornado.web import RequestHandler
from handler.exceptions import *
import json

DEFAULT_TYPE = []

class BaseHandler(RequestHandler):

	@property
	def dns_db(self):
		return self.settings["db"][0]

	@property
	def ipcis_db(self):
		return self.settings["db"][1]

	@property
    def json_body(self):
        if not hasattr(self, '_json_body'):
            if hasattr(self.request, "body"):
                try:
                    if not self.request.body:
                        self._json_body = {}
                    else:
                        self._json_body = json.loads(self.request.body.decode('utf-8'))
                except ValueError:
                    raise ArgsError("参数不是json格式！")
        return self._json_body

	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "Access-Token, Content-Type")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def finish_success(self, **kwargs):
		rs = {
			"status": "success",
			"result": list(kwargs.values())[0]
		}
		self.finish(json.dumps(rs))

	def finish_err(self, **kwargs):
		rs = {
			"status": "err",
			"result": list(kwargs.values())[0]
		}
		self.finish(json.dumps(rs))

	def get_argument(self, name, default=DEFAULT_TYPE, strip=True):
        if self.json_body:
            if name in self.json_body:
                rs = self.json_body[name]
                return rs
            elif default is DEFAULT_TYPE:
                raise MissingArgumentError(name)
            else:
                return default
        else:
            return super(BaseHandler, self).get_argument(name, default, strip)