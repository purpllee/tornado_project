# coding:utf-8


import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import config
import torndb
import redis

from tornado.options import define, options

from urls import handlers

define("port",default=8000, type=int)
class Application(tornado.web.Application):
    def __init__(self, *args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        # self.db = torndb.Connection(
        #     host=config.mysql_options["host"],
        #     database = config.mysql_options["database"],
        #     user= config.mysql_options["user"],
        #     password=config.mysql_options["password"],
        # )
        self.db = torndb.Connection(**config.mysql_options)
        # self.redis = redis.StrictRedis(
        #     host=config.redis_options["host"],
        #     port = config.redis_options["port"],
        # )
        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    # 可以修改显示的log等级
    options.logging = config.log_level
    # 指定log文件地址
    # options.log_file_prefix = config.log_file
    tornado.options.parse_command_line()
    app =Application(
        handlers, **config.setting
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()