import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpclient
import tornado.gen

import os.path
import urllib
import urllib2
import json
from login import LoginHandler, LogoutHandler, WelcomeHandler

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,"http://m.baidu.com/api?action=search&word=*&apilevel=18&bdi_bear=WF&bdi_cid=9177265119920&bdi_imei=XWvGSz2%252F6IEu3xlWyyVa%252BQ%253D%253D&bdi_imsi=NWEzYjI4N2YyYjEzYmVmOA%3D%3D&bdi_loc=5YyX5Lqs5biC&bdi_mac=YWM6YmM6MzI6OWE6YmY6MzM%3D&bdi_uip=127.0.0.1&brand=OPSSON&cname=WS%3AYY&cpack=monkey&ct=1452249585&cver=&docid=9403459&dpi=300&from=1018654f&model=Q1&os_version=4.3&pver=3&refer_tag=rec&req_biz=1&resolution=720_1280&show_time=1452249585&token=jingyan&type=app&ua=opera&uid=712ACBBE63076AEC76BE860AQDEWE880&sign=CAC16505BC1964A2C4310707AD395DB4&action=appdetail&format=json")
        body = json.loads(response.body)
        self.write(body)
        self.finish()

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
        (r'/', IndexHandler),
        (r'/modify', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

