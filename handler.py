#!/usr/bin/env python
# encoding: utf-8
__author__ = 'louis'

from rediscluster import StrictRedisCluster
from utils import singleton


@singleton
class RedisHandler(object):
    cluster = {'nodes':{'node_1':{"host": "127.0.0.1", "port": "7000"}}}
    rc = StrictRedisCluster(cluster=cluster, db=0, mastersonly=True)

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