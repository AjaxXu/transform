#!/usr/bin/env python
# encoding: utf-8
__author__ = 'louis'

from Crypto.Cipher import AES
import hashlib
import urllib
import base64

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class EncryptUtil(object):
    def get_md5_value(self, src):
        myMd5 = hashlib.md5()
        myMd5.update(src)
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    def _pad(self, s): return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    def _cipher(self):
        key = '65f1c15f5a46745f451ab4ad'
        iv = 'bd367d1130f11d8c'
        fromvalue = '1019356a'
        md5 = self.get_md5_value(fromvalue + key)
        md5 = md5[-16:].upper()
        # print md5
        if len(iv) < 16:
            iv = iv + (16 - len(iv)) * "\0"
        # print iv
        return AES.new(key=md5, mode=AES.MODE_CBC, IV=iv)

    def encrypt_token(self, data):
        return self._cipher().encrypt(self._pad(data))

    def decrypt_token(self, data):
        return self._cipher().decrypt(data)

@singleton
class UrlUtil(object):
    def getUrl(self, dic, token):
        encode = base64.b64encode(EncryptUtil().encrypt_token(token))
        encode = urllib.quote(encode)
        dic['bdi_imei'] = encode
        for k in dic.keys():
            dic[k] = urllib.quote(dic[k])
        dicsort = sorted(dic.keys())
        url = 'http://m.baidu.com/api?'
        for app_id in dicsort:
            url = url + app_id + '=' + dic[app_id] + '&'
        # url = urllib.quote(url)
        url = url[:-1]
        return url

@singleton
class EncodeUtil(object):
    def unicodeToStr(self, value):
        if isinstance(value, unicode):
            try:
                return value.encode("utf-8")
            except UnicodeEncodeError:
                pass
        return value