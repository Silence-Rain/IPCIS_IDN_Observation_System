import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
import routes
from config import *
from MySQL.mysql import MySQL

define("port", default=8888, help="本地监听端口", type=int)
define("DEBUG", default=True, help="是否开启debug模式", type=bool)
define("TEST", default=True, help="测试服务器,支持跨域访问,推送测试模式", type=bool)
tornado.options.parse_command_line()

dns_db = MySQL(
		host=DNS_HOST,
		user=DNS_USER,
		passwd=DNS_PASSWD,
		port=DNS_PORT,
		db=DNS_DB
	)
ipcis_db = MySQL(
		host=IPCIS_HOST,
		user=IPCIS_USER,
		passwd=IPCIS_PASSWD,
		db=IPCIS_DB
	)

application = tornado.web.Application(
		handlers=routes.handlers,
		db=[dns_db, ipcis_db],
		TEST=options.TEST,
		debug=options.DEBUG,
    	autoreload=True,
	)

if __name__ == '__main__':
	application.listen(options.port)
	ioloop = tornado.ioloop.IOLoop.current()
	ioloop.start()