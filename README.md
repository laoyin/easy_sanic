gunicorn app:app --bind 0.0.0.0:7001 --worker-class sanic.worker.GunicornWorker -w 2

easy sanic 框架，集成了sanic，同时自定义async orm， （目前支持postgres）
easyrestful。简单好用，你可以完全不用掌握python3 aysncio相关知识 也能写出高性能服务。

easy sanic 目标是 快速打造微服务。

easy sanic framework.


创建项目入口：
app.py
```python

import asyncio
import opentracing
from sanic import Sanic
from aioredis import create_redis_pool

from easy_sanic.utils.ascci_helper import init_text
from easy_sanic.utils.jwt_helper import JwtHelper
from easy_sanic.utils.aio_redis import SanicRedis
from easy_sanic.db.db import ConnectionPool

# 此处url 为之定义url文件，需要自己添加，文档有介绍如何引用
from url import app_url

app = Sanic(__name__)

app.config.update({
    'DB_CONFIG':{
        'user':'postgres',
        'password':'password',
        'database':'',
        'host':'',
        'port':''
    }
})
redis_conf = {
            'REDIS':{
                'address': ("REDIS_HOST", "REDIS_PORT"),
                'db': "REDIS_DB",
            }
        }

redis_conf['REDIS']['password'] = "REDIS_PASSWORD"

app.config.update(redis_conf)


@app.listener('before_server_start')
async def before_server_start(app, loop):
    # 引用url
    app_url(app)
    queue = asyncio.Queue()
    app.queue = queue
    app.db = await ConnectionPool(loop=loop).init(app.config['DB_CONFIG'])

    _c = dict(loop=loop)
    config = app.config.get('REDIS')
    for key in ['address', 'db', 'password', 'ssl', 'encoding', 'minsize',
                'maxsize', 'create_connection_timeout']:
        if key in config:
            _c.update({key: config.get(key)})
    _redis = await create_redis_pool(**_c)

    app.redis = _redis
    app.conn = _redis


@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    app.redis.close()
    await app.redis.wait_closed()
    await app.service.deregister()
    app.queue.join()

if __name__ == '__main__':
    print(init_text)
    app.run(host='0.0.0.0', port=7001)
```


如何定义url：

url:
```python
from yourview.py import YourClass
def app_url(app):
    app.router.add(uri='/hello', methods=['GET'], handler=YourClass().as_views)

```

```python
'''yourviews.py'''
from sanic.response import json
from easy_sanic.restful.operation_handler import ResourceBase, operation

class RestStatus:

    @classmethod
    def response_status(cls, ret, message, data=""):
        return json({"ret": ret, "message": message, "data":data})


class YourClass(ResourceBase):

    async def get(self, request):
        return RestStatus.response_status(200, "ok", data=data)

    async def post(self, request):
        request_data = request.form
        return RestStatus.response_status(200, "ok", data=data)

    def delete(self, request):
        print("i am delete")
        return RestStatus.response_status(400, "request method error")

    @operation(flag=True)
    def custom_url(self, request):
        print("i am print hh")

        return RestStatus.response_status(400, "request method error")

    @operation(flag=False)
    def hello(self, request):
        print("afwefaewfaw")
        return RestStatus.response_status(200, "pengfeng")


```

现在你可以通过url 进行 get、post、delete 访问了，支持http（get、post、delete、put）
同时可以自定义方法

使用operation， flag=True 为get方法， False 为 post方法，使用如下：


http://127.0.0.1:port/hello?operation=custom_url




如何定义orm models：
orm:
models.py
```python
from easy_sanic.db.orm import SqlObject, FieldObject, TableName

#User message
class User(metaclass=SqlObject):
    id = FieldObject('id', 'varchar(200) primary key')
    name = FieldObject('name', 'varchar(200)')
    password = FieldObject('password', 'varchar(200)')
    table_name = TableName('users')

```


如何使用model orm


在view 里面
```python
from easy_sanic.restful.operation_headler import ResourceBase, operation


class ProvilegeRole(ResourceBase):

    async def get(self, request):
        data = await User.filter(request, id='yinxingpan')
        new_obj = User(id="yinxingpan", name="haha2", password="123")
        result = await new_obj.save(request)
        print(data)
        return RestStatus.response_status(200, "ok", data=data)

```

其中 model.filter、model.save  必须传递request方法




目前支持postgres，redis

redis的使用：
```python
with await request.app.conn as conn:
    # await conn.get("NOT_RESTRICT_URL") restrict
    url_status = await conn.execute('SISMEMBER', "key", "value")
```



