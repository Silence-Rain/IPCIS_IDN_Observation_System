import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
import routes

define("port", default=8889, help="本地监听端口", type=int)
define("DEBUG", default=True, help="是否开启debug模式", type=bool)
define("TEST", default=False, help="测试服务器,支持跨域访问,推送测试模式", type=bool)
tornado.options.parse_command_line()

application = tornado.web.Application(
		handlers=routes.handlers,
		TEST=options.TEST,
		debug=options.DEBUG,
		autoreload=True,
	)

if __name__ == '__main__':
	application.listen(options.port)
	ioloop = tornado.ioloop.IOLoop.current()
	ioloop.start()