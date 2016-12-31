#!/usr/bin/env python
# encoding: utf-8
__author__ = 'louis'

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpclient
import tornado.gen
import base64
import urllib

from webargs import fields
from webargs.tornadoparser import use_args

from rediscluster import StrictRedisCluster
from utils import singleton
import json
from utils import EncryptUtil, EncodeUtil


@singleton
class RedisHandler(object):
    startup_nodes = [{"host": "127.0.0.1", "port": "6379"}]
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    def getValue(self, key):
        timeout = self.rc.ttl(key)
        if timeout >= -1:
            result = self.rc.get(key)
            self.rc.expire(key, timeout + 60)
            return result
        return None

    def setValue(self, key, value):
        self.rc.set(key, value)
        self.rc.expire(key, 60)

class BaseHandler(tornado.web.RequestHandler):
    def request_body(self, args, action, token):
        encode = base64.b64encode(EncryptUtil().encrypt_token(token))
        encode = urllib.quote(encode)
        args['bdi_imei'] = encode
        for k in args.keys():
            args[k] = urllib.quote(EncodeUtil().unicodeToStr(args[k]))
        dicsort = sorted(args.keys())
        url = ''
        for app_id in dicsort:
            url = url + app_id + '=' + args[app_id] + '&'
        url = url[:-1]
        sign = EncryptUtil().get_md5_value(url).upper()

        redisHandler = RedisHandler()
        body = redisHandler.getValue(sign)
        if body == None:
            url = url + '&sign=' + sign + '&' + 'action='+ action+'&format=json'
            url = 'http://m.baidu.com/api?' + url
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(client.fetch, url)
            body = response.body
            redisHandler.setValue(sign, body)
        body = json.loads(EncodeUtil().unicodeToStr(body))
        return body

# search
class SearchHandler(BaseHandler):
    search_args = {
        'from': fields.Str(required=True, missing='1019356a'),
        'token': fields.Str(required=True, missing='qqllqyfbx'),
        'type': fields.Str(required=True, missing='app'),
        'word': fields.Str(required=True),
        'bdi_loc': fields.Str(required=True, missing='5YyX5Lqs5biC'),
        'bdi_uip': fields.Str(required=True, missing='113.142.37.167'),
        'bdi_bear': fields.Str(required=True, missing='WF'),
        'resolution': fields.Str(required=True, missing='720_1280'),
        'dpi': fields.Str(required=True, missing='320'),
        'apilevel': fields.Str(required=True, missing='18'),
        'os_version': fields.Str(required=True, missing='4.3'),
        'brand': fields.Str(required=True, missing='OPSSON'),
        'model': fields.Str(required=True, missing='Q1'),
        'pver': fields.Str(required=True, missing='3'),
        'uid': fields.Str(missing='712ACBBE63076AEC76BE860AQDEWE880'),
        'pn': fields.Str(missing='0'),
        'rn': fields.Str(missing='10'),
        'bdi_mac': fields.Str(missing='YWM6YmM6MzI6OWE6YmY6MzM='),
        'bdi_cid': fields.Str(missing='9177265119920'),
        'bdi_imsi': fields.Str(missing='NWEzYjI4N2YyYjEzYmVmOA=='),
        'ct': fields.Str(missing='1452249585'),
        'cname': fields.Str(missing='WS'),
        'cver': fields.Str(missing='2.0'),
        'cpack': fields.Str(missing='monkey'),
    }

    @tornado.web.asynchronous
    @tornado.gen.engine
    @use_args(search_args)
    def get(self, args):
        token = '862879000296806'
        body = self.request_body(args, 'search', token)
        self.write(body)
        self.finish()

# package
class PackageHandler(BaseHandler):

    package_args = {
        'from': fields.Str(required=True, missing='1019356a'),
        'token': fields.Str(required=True, missing='qqllqyfbx'),
        'type': fields.Str(required=True, missing='app'),
        'package': fields.Str(required=True),
        'req_biz': fields.Str(required=True, missing='1'),
        'bdi_loc': fields.Str(required=True, missing='5YyX5Lqs5biC'),
        'bdi_uip': fields.Str(required=True, missing='113.142.37.167'),
        'bdi_bear': fields.Str(required=True, missing='WF'),
        'resolution': fields.Str(required=True, missing='720_1280'),
        'dpi': fields.Str(required=True, missing='320'),
        'apilevel': fields.Str(required=True, missing='18'),
        'os_version': fields.Str(required=True, missing='4.3'),
        'brand': fields.Str(required=True, missing='OPSSON'),
        'model': fields.Str(required=True, missing='Q1'),
        'pver': fields.Str(required=True, missing='3'),
        'ua': fields.Str(required=True, missing='android4.3'),
        'show_time': fields.Str(required=True, missing='1452249585'),
        'refer_tag': fields.Str(required=True, missing='board'),
        'uid': fields.Str(missing='712ACBBE63076AEC76BE860AQDEWE880'),
        'bdi_mac': fields.Str(missing='YWM6YmM6MzI6OWE6YmY6MzM='),
        'bdi_cid': fields.Str(missing='9177265119920'),
        'bdi_imsi': fields.Str(missing='NWEzYjI4N2YyYjEzYmVmOA=='),
        'ct': fields.Str(missing='1452249585'),
        'cname': fields.Str(missing='WS'),
        'cver': fields.Str(missing='2.0'),
        'cpack': fields.Str(missing='monkey'),
    }

    @tornado.web.asynchronous
    @tornado.gen.engine
    @use_args(package_args)
    def get(self, args):
        token = '862879000296806'
        # token = self.get_argument('token').encode("utf-8")
        # encode = base64.b64encode(EncryptUtil().encrypt_token(token))
        # encode = urllib.quote(encode)
        # args['bdi_imei'] = encode
        # for k in args.keys():
        #     args[k] = urllib.quote(EncodeUtil().unicodeToStr(args[k]))
        # dicsort = sorted(args.keys())
        # url = ''
        # for app_id in dicsort:
        #     url = url + app_id + '=' + args[app_id] + '&'
        # url = url[:-1]
        # sign = EncryptUtil().get_md5_value(url).upper()
        #
        # redisHandler = RedisHandler()
        # body = redisHandler.getValue(sign)
        # if body == None:
        #     url = url + '&sign=' + sign + '&' + 'action=appdetail&format=json'
        #     url = 'http://m.baidu.com/api?' + url
        #     client = tornado.httpclient.AsyncHTTPClient()
        #     response = yield tornado.gen.Task(client.fetch, url)
        #     body = response.body
        #     redisHandler.setValue(sign, body)
        # body = json.loads(EncodeUtil().unicodeToStr(body))
        body = self.request_body(args, 'appdetail', token)
        self.write(body)
        self.finish()

# Docid
class DocidHandler(BaseHandler):
    docid_args = {
        'from': fields.Str(required=True, missing='1019356a'),
        'token': fields.Str(required=True, missing='qqllqyfbx'),
        'type': fields.Str(required=True, missing='app'),
        'docid': fields.Str(required=True),
        'req_biz': fields.Str(required=True, missing='1'),
        'bdi_loc': fields.Str(required=True, missing='5YyX5Lqs5biC'),
        'bdi_uip': fields.Str(required=True, missing='113.142.37.167'),
        'bdi_bear': fields.Str(required=True, missing='WF'),
        'resolution': fields.Str(required=True, missing='720_1280'),
        'dpi': fields.Str(required=True, missing='320'),
        'apilevel': fields.Str(required=True, missing='18'),
        'os_version': fields.Str(required=True, missing='4.3'),
        'brand': fields.Str(required=True, missing='OPSSON'),
        'model': fields.Str(required=True, missing='Q1'),
        'pver': fields.Str(required=True, missing='3'),
        'ua': fields.Str(required=True, missing='android4.3'),
        'show_time': fields.Str(required=True, missing='1452249585'),
        'refer_tag': fields.Str(required=True, missing='board'),
        'uid': fields.Str(missing='712ACBBE63076AEC76BE860AQDEWE880'),
        'bdi_mac': fields.Str(missing='YWM6YmM6MzI6OWE6YmY6MzM='),
        'bdi_cid': fields.Str(missing='9177265119920'),
        'bdi_imsi': fields.Str(missing='NWEzYjI4N2YyYjEzYmVmOA=='),
        'ct': fields.Str(missing='1452249585'),
        'cname': fields.Str(missing='WS'),
        'cver': fields.Str(missing='2.0'),
        'cpack': fields.Str(missing='monkey'),
    }

    @tornado.web.asynchronous
    @tornado.gen.engine
    @use_args(docid_args)
    def get(self, args):
        token = '862879000296806'
        body = self.request_body(args, 'appdetail', token)
        self.write(body)
        self.finish()