#!/usr/bin/env python
# encoding: utf-8

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
from utils import UrlUtil, EncryptUtil
from handler import RedisHandler
from login import LoginHandler, LogoutHandler, WelcomeHandler

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

# search
class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        word = self.get_argument('word').encode("utf-8")
        redisHandler = RedisHandler()
        key = EncryptUtil.get_md5_value('search' + word)
        body = redisHandler.getValue(key)
        if body == None :
            dic = {'from': '1019356a', 'token': 'qqllqyfbx', 'type': 'app',
                   'bdi_loc': '5YyX5Lqs5biC', 'bdi_uip': '113.142.37.167', 'bdi_bear': 'WF', 'resolution': '720_1280',
                   'dpi': '320', 'apilevel': '18', 'os_version': '4.3', 'brand': 'OPSSON', 'model': 'Q1', 'pver': '3',
                   'uid': '712ACBBE63076AEC76BE860AQDEWE880', 'pn': '0', 'rn': '10',
                   'bdi_cid': '9177265119920', 'bdi_mac': 'YWM6YmM6MzI6OWE6YmY6MzM=',
                   'bdi_imsi': 'NWEzYjI4N2YyYjEzYmVmOA==',
                   'ct': '1452249585', 'cname': 'WS', 'cver': '2.0', 'cpack': 'monkey'}
            sign = '80E04B6A82A481489CD4135729283A96'
            action = 'search'
            token = '862879000296806'
            dic['word'] = word.encode("utf-8")
            dic['sign'] = sign
            dic['action'] = action
            dic['format'] = 'json'
            url = UrlUtil().getUrl(dic, token)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(client.fetch,url)
            body = json.loads(response.body)
            redisHandler.setValue(key, body)
        self.write(body)
        self.finish()

# package
class PackageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        package = urllib.unquote(self.get_argument('package'))
        redisHandler = RedisHandler()
        key = EncryptUtil.get_md5_value('package' + package)
        body = redisHandler.getValue(key)
        if body == None:
            dic = {'from': '1019356a', 'token': 'qqllqyfbx', 'type': 'app', 'req_biz': '1',
                   'bdi_loc': '5YyX5Lqs5biC', 'bdi_uip': '113.142.37.167', 'bdi_bear': 'WF', 'resolution': '720_1280',
                   'dpi': '320', 'apilevel': '18', 'os_version': '4.3', 'brand': 'OPSSON', 'model': 'Q1', 'pver': '3',
                   'uid': '712ACBBE63076AEC76BE860AQDEWE880', 'ua': 'android4.3', 'show_time': '1452249585',
                   'refer_tag': 'board',
                   'bdi_cid': '9177265119920', 'bdi_mac': 'YWM6YmM6MzI6OWE6YmY6MzM=',
                   'bdi_imsi': 'NWEzYjI4N2YyYjEzYmVmOA==',
                   'ct': '1452249585', 'cname': 'WS', 'cver': '2.0', 'cpack': 'monkey'}
            sign = 'FDA42A26A5DE26342E84B99AA657FC15'
            action = 'appdetail'
            token = '862879000296806'
            dic['sign'] = sign
            dic['action'] = action
            dic['format'] = 'json'
            dic['package'] = package.encode("utf-8")
            url = UrlUtil().getUrl(dic, token)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(client.fetch,url)
            body = json.loads(response.body)
            redisHandler.setValue(key, body)
        self.write(body)
        self.finish()

# Docid
class DocidHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        docid = urllib.unquote(self.get_argument('docid'))
        redisHandler = RedisHandler()
        key = EncryptUtil.get_md5_value('docid' + docid)
        body = redisHandler.getValue(key)
        if body == None:
            dic = {'from': '1019356a', 'token': 'qqllqyfbx', 'type': 'app', 'req_biz': '1',
                   'bdi_loc': '5YyX5Lqs5biC', 'bdi_uip': '113.142.37.167', 'bdi_bear': 'WF', 'resolution': '720_1280',
                   'dpi': '320', 'apilevel': '18', 'os_version': '4.3', 'brand': 'OPSSON', 'model': 'Q1', 'pver': '3',
                   'uid': '712ACBBE63076AEC76BE860AQDEWE880', 'ua': 'android4.3', 'show_time': '1452249585',
                   'refer_tag': 'board',
                   'bdi_cid': '9177265119920', 'bdi_mac': 'YWM6YmM6MzI6OWE6YmY6MzM=',
                   'bdi_imsi': 'NWEzYjI4N2YyYjEzYmVmOA==',
                   'ct': '1452249585', 'cname': 'WS', 'cver': '2.0', 'cpack': 'monkey'}
            sign = 'D144E2E3364B275568372FFE80DE133E'
            action = 'appdetail'
            token = '862879000296806'
            dic['docid'] = docid.encode("utf-8")
            dic['sign'] = sign
            dic['action'] = action
            dic['format'] = 'json'
            url = UrlUtil().getUrl(dic, token)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(client.fetch,url)
            body = json.loads(response.body)
            redisHandler.setValue(key, body)
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

