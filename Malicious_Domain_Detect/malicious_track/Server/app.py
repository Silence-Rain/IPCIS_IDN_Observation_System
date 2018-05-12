import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
import routes
from MySQL.mysql import MySQL

define("port", default=8888, help="本地监听端口", type=int)
define("DEBUG", default=True, help="是否开启debug模式", type=bool)
define("TEST", default=True, help="测试服务器,支持跨域访问,推送测试模式", type=bool)
tornado.options.parse_command_line()

dns_db = MySQL(
		host="211.65.193.193",
		user="ipcis",
		passwd="",
		port="3307",
		db="IPCIS_DNS_DB"
	)
ipcis_db = MySQL(
		host="211.65.193.23",
		user="root",
		passwd="admin246531",
		db="known_malicious"
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