#coding=utf-8
import uuid
import hashlib
from sanic import response
from sanic.response import json

import settings
from utils.jwt_helper import JwtHelper
from utils.utils import generate_slat, RestStatus
from db.dao import User
from restful.operation_headler import ResourceBase, operation


class ProvilegeRole(ResourceBase):

    async def get(self, request):
        data = await User.filter(request, id='yinxingpan')
        new_obj = User(id="yinxingpan", name="haha2", password="123")
        result = await new_obj.save(request)
        print(data)
        return RestStatus.response_status(200, "ok", data=data)

    async def post(self, request):
        request_data = request.form
        return RestStatus.response_status(200, "ok", data=data)

    def delete(self, request):
        print("i am delete")

        return RestStatus.response_status(400, "request method error")

    @operation(flag=True)
    def print_hh(self, request):
        print("i am print hh")

        return RestStatus.response_status(400, "request method error")

    @operation(flag=True)
    def hello(self, request):
        print("afwefaewfaw")
        return RestStatus.response_status(200, "pengfeng")


class PrivilegeService:
    async def get(self, request):
        pass


    async def post(self, request):
        request_data = request.form
        try:
            name = request_data['name'][0]
        except KeyError as e:
            return RestStatus.response_status(301, "parameter error")
        except Exception as e:
            return RestStatus.response_status(301, "parameter error")

        if not all([name]):
            return RestStatus.response_status(301, "parameter error")

        sql = "SELECT * FROM xauth_role WHERE name=$1"
        insert_sql = "INSERT INTO xauth_role(id, name) values($1, $2)"
        async with request.app.db.transaction(request) as cur:
            data = await cur.fetch(sql, name)
            if data:
                return RestStatus.response_status(401, "already exist role")
            id = str(uuid.uuid1())
            data = await cur.execute(insert_sql, id, name)
            if data:
                return RestStatus.response_status(200, "ok")
            else:
                return RestStatus.response_status(300, "insert error")

    async def delete(self):
        pass


class PrivilegeAPI:

    async def get(self, request):
        pass


    async def post(self, request):
        request_data = request.form
        try:
            name = request_data['name'][0]
            open = request_data['open'][0]
        except KeyError as e:
            return RestStatus.response_status(301, "parameter error")
        except Exception as e:
            return RestStatus.response_status(301, "parameter error")

        if not all([name, open]):
            return RestStatus.response_status(301, "parameter error")

        sql = "SELECT * FROM xauth_role WHERE name=$1"
        insert_sql = "INSERT INTO xauth_role(id, name) values($1, $2)"
        async with request.app.db.transaction(request) as cur:
            data = await cur.fetch(sql, name)
            if data:
                return RestStatus.response_status(401, "already exist role")
            id = str(uuid.uuid1())
            data = await cur.execute(insert_sql, id, name)
            if open:
                with request.app.conn as conn:
                    url_status = await conn.execute('SADD', settings.xauth_api_allow_all, url)

            if data:
                return RestStatus.response_status(200, "ok")
            else:
                return RestStatus.response_status(300, "insert error")


    async def delete(self, request):
        request_data = request.form
        try:
            id = request_data['id'][0]
        except KeyError as e:
            return RestStatus.response_status(301, "parameter error")
        except Exception as e:
            return RestStatus.response_status(301, "parameter error")

        if not all([id]):
            return RestStatus.response_status(301, "parameter error")

        sql = "SELECT * FROM xauth_api WHERE id=$1"
        delete_sql = "delete from xauth_api where id=$1"
        async with request.app.db.transaction(request) as cur:
            data = await cur.fetch(sql, name)
            if not data:
                return RestStatus.response_status(401, "not exist api")

            data = await cur.execute(delete_sql, id)
            if data:
                return RestStatus.response_status(200, "ok")
            else:
                return RestStatus.response_status(300, "delete error")



class PrivilegePermission:
    async def get(self, request):
        pass


    async def post(self, request):
        request_data = request.form
        try:
            role_name = request_data['role_name'][0]
            api_id = request_data['api_id'][0]
        except KeyError as e:
            return RestStatus.response_status(301, "parameter error")
        except Exception as e:
            return RestStatus.response_status(301, "parameter error")

        if not all([name]):
            return RestStatus.response_status(301, "parameter error")

        sql = "SELECT * FROM xauth_permission WHERE role_name=$1 and api_id=$2"
        api_sql = "SELECT name, url FROM xauth_api WHERE id=$1"
        insert_sql = "INSERT INTO xauth_permission(id, name) values($1, $2)"
        async with request.app.db.transaction(request) as cur:
            data = await cur.fetch(sql, name)
            if data:
                return RestStatus.response_status(401, "already exist role")
            id = str(uuid.uuid1())
            data = await cur.execute(insert_sql, id, name)
            if data:
                service_redis_key = settings.xauth_server_privileage.format(role=user_role, service=service)
                with await request.app.conn as conn:
                    url_status = await conn.execute('SADD', service_redis_key, url)
                return RestStatus.response_status(200, "ok")
            else:
                return RestStatus.response_status(300, "insert error")