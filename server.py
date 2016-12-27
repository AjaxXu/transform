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

# search
class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,"http://m.baidu.com/api?apilevel=19&bdi_bear=WF&bdi_cid=9177265119920&bdi_imei=LRJ60LZNQgHG8DYc9BOFng%253D%253D&bdi_imsi=NWEzYjI4N2YyYjEzYmVmOA%3D%3D&bdi_loc=5YyX5Lqs5biC&bdi_mac=YWM6YmM6MzI6OWE6YmY6MzM%3D&bdi_uip=113.142.37.167&brand=OPSSON&cname=WS%3AYY&cpack=monkey&ct=1452249585&cver=2.0&dpi=320&from=1019356a&model=Q1&os_version=4.3&pn=0&pver=3&resolution=720_1280&rn=10&token=qqllqyfbx&type=app&uid=712ACBBE63076AEC76BE860AQDEWE880&word=%E5%BE%AE%E4%BF%A1&sign=E85A6EF76190D4191F20F66F98670B33&action=search&format=json")
        body = json.loads(response.body)
        self.write(body)
        self.finish()

# package
class PackageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,"http://m.baidu.com/api?apilevel=19&bdi_bear=WF&bdi_cid=9177265119920&bdi_imei=LRJ60LZNQgHG8DYc9BOFng%253D%253D&bdi_imsi=NWEzYjI4N2YyYjEzYmVmOA%3D%3D&bdi_loc=5YyX5Lqs5biC&bdi_mac=YWM6YmM6MzI6OWE6YmY6MzM%3D&bdi_uip=113.142.37.167&brand=OPSSON&cname=WS%3AYY&cpack=monkey&ct=1452249585&cver=2.0&dpi=320&from=1019356a&model=Q1&os_version=4.3&package=com.tencent.mm&pver=3&refer_tag=rec&req_biz=1&resolution=720_1280&show_time=1452249585&token=qqllqyfbx&type=app&ua=android4.3&uid=712ACBBE63076AEC76BE860AQDEWE880&sign=C0680B0DCBAA812B3204377D5A4F18B5&action=appdetail&format=json")
        body = json.loads(response.body)
        self.write(body)
        self.finish()

# Docid
class DocidHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,"http://m.baidu.com/api?apilevel=19&bdi_bear=WF&bdi_cid=9177265119920&bdi_imei=LRJ60LZNQgHG8DYc9BOFng%253D%253D&bdi_imsi=NWEzYjI4N2YyYjEzYmVmOA%3D%3D&bdi_loc=5YyX5Lqs5biC&bdi_mac=YWM6YmM6MzI6OWE6YmY6MzM%3D&bdi_uip=113.142.37.167&brand=OPSSON&cname=WS%3AYY&cpack=monkey&ct=1452249585&cver=2.0&docid=10589832&dpi=320&from=1019356a&model=Q1&os_version=4.3&pver=3&refer_tag=rec&req_biz=1&resolution=720_1280&show_time=1452249585&token=qqllqyfbx&type=app&ua=android4.3&uid=712ACBBE63076AEC76BE860AQDEWE880&sign=316B977B1D1E811B18DBC5855094C525&action=appdetail&format=json")
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
        (r'/search', SearchHandler),
        (r'/package', PackageHandler),
        (r'/docid', DocidHandler),
        (r'/modify', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

