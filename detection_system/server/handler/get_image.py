#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
import base64
import hashlib
import time
import datetime

class ImageHandler(BaseHandler):

	async def post(self):
		raw = self.get_argument("img").split("base64,")[1]
		img = base64.b64decode(raw)
		m = hashlib.md5()
		m.update(bytes(str(time.time()),encoding='utf-8'))

		with open("data/%s-%s.png" % (str(datetime.date.today()), m.hexdigest()[:6]), "wb") as f:
			f.write(img)

		self.finish_success(result=True)


routes.handlers += [
	(r'/saveImage', ImageHandler)
]
 