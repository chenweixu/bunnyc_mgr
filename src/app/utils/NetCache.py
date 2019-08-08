import redis
from app.main.conf import conf_data

class NetCache(object):
    """docstring for NetCache"""
    def __init__(self):
        super(NetCache, self).__init__()
        redis_host = conf_data('redis', 'host')
        redis_port = conf_data('redis', 'port')
        self.r = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            decode_responses=True)

        self.NginxLockSet = 'set:nginxlockip'

    def setAdd(self, value):
        self.r.sadd(self.NginxLockSet, value)

    def setRemove(self, value):
        self.r.srem(self.NginxLockSet, value)

    def setSmembers(self):
        '''获取集合全部数据'''
        return self.r.smembers(self.NginxLockSet)

    def setDel(self):
        return self.r.delete(self.NginxLockSet)
