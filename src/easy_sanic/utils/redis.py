#-*- coding: utf-8 -*-
from redis import ConnectionPool, Redis
import pdb,json
import settings

REDIS_MAX_CONNECTION = 500
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = 6379
REDIS_DB = 0

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


#单例
@singleton
class RedisListTool(object):
    def __init__(self):
        self.__connection_pool = ConnectionPool(max_connections=REDIS_MAX_CONNECTION, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.__redis = self.get_redis()
        # self.conn = self.__redis

    # 保存一条记录，默认添加到最前面
    def save_key_value(self, key, value, append=False):
        if append:
            self.__redis.rpush(key, value)
        else:
            self.__redis.lpush(key, value)

    # 保存多条记录，默认添加到最前面
    def save_key_values(self, key, value_list, append=False):
        if not isinstance(value_list, list) and not isinstance(value_list, tuple):
            return
        if len(value_list) <= 0:
            return
        if append:
            self.__redis.rpush(key, *value_list)
        else:
            self.__redis.lpush(key, *value_list)

    # 获取一条记录
    def get_key_value(self, key, index):
        value = self.__redis.lindex(key, index)
        return value

    # 获取多条记录
    def get_key_values(self, key, start=0, end=-1):
        values = self.__redis.lrange(key, start, end)
        return values

    # 获取键对应记录集的长度
    def get_key_values_length(self, key):
        length = self.__redis.llen(key)
        return length

    # 删除一条记录
    def delete_key_value(self, key, value):
        self.__redis.lrem(key, value)

    # 删除多条记录
    def delete_key_values(self, key, value_list):
        for value in value_list:
            self.__redis.lrem(key, value)

    # 删除一个key
    def delete_key(self, key):
        self.__redis.delete(key)

    # key是否存在
    def has_key(self, key):
        return self.__redis.exists(key)

    # 创建一个key,并添加值(如果key存在，则先删除再创建)
    def create_key_values(self, key, value_list, append=False):
        if self.has_key(key):
            self.delete_key(key)
        self.save_key_values(key, value_list, append)

    # 获得一个redis实例
    def get_redis(self):
        return Redis(connection_pool=self.__connection_pool)

    #创建一个key-value  value为可序列化的字典 -------cpr 3.15
    def set_redis_key_values(self, key, value):
        from xieli.util.utils import convert_to_dict
        if self.has_key(key):
            self.delete_key(key)
        dic_value = convert_to_dict(value)
        self.__redis.set(key, json.dumps(dic_value))

    #创建一个key-value
    def set_redis_key_value(self, key, value):
        self.__redis.set(key,value)

    #通过一个key 获取 value
    def get_value_by_key(self, key):
        return self.__redis.get(key)

    #通过一个keys 获取 values
    def mget_value_by_keys(self, keys):
        result = []
        value_list = self.__redis.mget(keys)
        for value in value_list:
            result.append(value)
        return result

    #获取一个key的value  value为可解析的json对象
    def get_redis_value(self, key):
        try:
            return json.loads(self.__redis.get(key))
        except:
            return self.__redis.get(key)

    #mget批量获取value
    def mget_redis_value(self, key_list):
        result = []
        value_list = self.__redis.mget(key_list)
        for value in value_list:
            try:
                result.append(json.loads(value))
            except:
                result.append(value)

        return result

    #设置具有过期时间的key
    def create_expries_key(self, key, value, expire_time):
        self.__redis.set(key, value)
        self.__redis.expire(key, expire_time)

    def incr(self, key):
        self.__redis.incr(key)

    def expire(self, key, expire_time):
        self.__redis.expire(key, expire_time)
