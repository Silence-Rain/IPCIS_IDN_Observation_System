#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
import base64

class ImageHandler(BaseHandler):

	async def post(self):
		raw = self.get_argument("img").split("base64,")[1]
		img = base64.b64decode(raw)

		with open("../test.png", "wb") as f:
			f.write(img)

		self.finish_success(result=True)


routes.handlers += [
	(r'/saveImage', ImageHandler)
]
 