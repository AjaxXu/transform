#!/usr/bin/env python
# encoding: utf-8


import tornado.gen

import os.path
from login import LoginHandler, LogoutHandler, WelcomeHandler
from handler import SearchHandler, PackageHandler, DocidHandler, DownloadHandler

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login"
    }

    application = tornado.web.Application([
        (r'/search', SearchHandler),
        (r'/package', PackageHandler),
        (r'/docid', DocidHandler),
        (r'/download', DownloadHandler),
        (r'/modify', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

