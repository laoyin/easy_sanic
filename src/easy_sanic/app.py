import asyncio
import opentracing
from sanic import Sanic
from sanic import response
from sanic.exceptions import abort
from sanic.response import json
from sanic.router import Router

import settings
from utils import utils
from utils.ascci_helper import init_text
from utils.jwt_helper import JwtHelper
from utils.aio_redis import SanicRedis
from db.db import ConnectionPool
from service import ServiceManager
from restfulapi import APIClient
from aioredis import create_redis_pool
from url import app_url
from db.init_sql_table import init_tables

app = Sanic(__name__)

app.config.update({
    'DB_CONFIG':{
        'user':'postgres',
        'password':'password',
        'database':'xauth',
        'host':'127.0.0.1',
        'port':'54321'
    },
    'CONSUL_AGENT_HOST':'127.0.0.1',
    'PORT':'7001'
})
redis_conf = {
            'REDIS':{
                'address': (settings.REDIS_HOST, settings.REDIS_PORT),
                'db': settings.REDIS_DB,
            }
        }
if settings.REDIS_PASSWORD:
    redis_conf['REDIS']['password'] = settings.REDIS_PASSWORD

app.config.update(redis_conf)


@app.listener('before_server_start')
async def before_server_start(app, loop):
    app_url(app)
    queue = asyncio.Queue()
    app.queue = queue
    app.client = APIClient(app)
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


@app.listener('after_server_start')
async def after_server_start(app, loop):
    service = ServiceManager(app.name, loop=loop, host=app.config['CONSUL_AGENT_HOST'])
    await service.register_service(app.config['PORT'])
    app.service = service


@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    app.redis.close()
    await app.redis.wait_closed()
    await app.service.deregister()
    app.queue.join()


# @app.middleware('request')
# async def cros(request):
#     if request.method == 'POST' or request.method == 'PUT':
#         request['span'] = None
#     request['span'] = None
#
#     service_class = app.client.url_map.get(request.path, None)
#     if not service_class:
#         return response.text("forbidden", status=403)
#     else:
#         service = service_class.get('rest_handler')
#
#     if not service:
#         return response.text("forbidden", status=403)
#
#     if request.method.lower() not in dir(service):
#         return response.text("method forbidden", status=403)
#
#     if request.method == 'POST':
#         res = await service.post(request)
#     elif request.method == 'GET':
#         res = await service.get(request)
#     elif request.method == 'DELETE':
#         res = await service.delete(request)
#     else:
#         res = await service.get(request)
#     return res


if __name__ == '__main__':
    print(init_text)
    app.run(host='0.0.0.0', port=7001)
