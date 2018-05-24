#!coding=utf8

from handler.base import BaseHandler
from handler.exceptions import *
import routes
import base64
import hashlib
import time
import datetime

class ImageHandler(BaseHandler):

	"""
		@api {get}	/saveImage  保存生成拓扑
		@apiGroup	save_image
		@apiVersion	1.0.0
		@apiDescription 自动在后台保存生成的通信活动拓扑
		@apiPermission all

		@apiSuccess	{String}	status	"success"
		@apiSuccess	{String}	result	"ok"
	"""

	async def post(self):
		raw = self.get_argument("img").split("base64,")[1]
		img = base64.b64decode(raw)
		m = hashlib.md5()
		m.update(bytes(str(time.time()),encoding='utf-8'))

		# 自动保存图片命名规则：yyyy-mm-dd-6位hash
		with open("data/%s-%s.png" % (str(datetime.date.today()), m.hexdigest()[:6]), "wb") as f:
			f.write(img)

		self.finish_success(result="ok")


routes.handlers += [
	(r'/saveImage', ImageHandler)
]
 