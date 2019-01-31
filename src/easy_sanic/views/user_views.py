#coding=utf-8
import uuid
import hashlib
from sanic import response
from sanic.response import json

import settings
from utils.jwt_helper import JwtHelper
from utils.utils import generate_slat, RestStatus


class User:

    def get(self, request):
        return response.text("nihao")

    def post(self, request):
        return response.text("nihao")

    def delete(self, request):
        return response.text("nihao")


class UserLogin:

    async def get(self, request):
        return response.text("forbidden")

    async def post(self, request):
        request_data = request.form
        try:
            name = request_data['name'][0]
            password = request_data['password'][0]
        except KeyError as e:
            return RestStatus.response_status(301, "parameter error")
        except Exception as e:
            return RestStatus.response_status(301, "parameter error")

        if not all([name, password]):
            return RestStatus.response_status(301, "parameter error")

        sql = "SELECT * FROM users WHERE name=$1"
        async with request.app.db.acquire(request) as cur:
            data = await cur.fetchrow(sql, name)
            if data:
                if hashlib.sha1((password+data['salt']).encode('utf8')).hexdigest() == data['password']:
                    token = JwtHelper.generate_token()
                    return RestStatus.response_status(200, "ok", data={'token':token})
                else:
                    return RestStatus.response_status(301, "user or password error")
            else:
                return RestStatus.response_status(301, "user or password error")


class UserRegister:

    async def post(self, request):
        request_data = request.form
        try:
            name = request_data['name'][0]
            password = request_data['password'][0]
        except KeyError as e:
            return RestStatus.response_status(301, "parameter error")
        except Exception as e:
            return RestStatus.response_status(301, "parameter error")

        if not all([name, password]):
            return RestStatus.response_status(301, "parameter error")

        salt = generate_slat()
        sql = "SELECT * FROM users WHERE name=$1"
        async with request.app.db.acquire(request) as cur:
            data = await cur.fetch(sql, name)
            if data:
                return RestStatus.response_status(302, "user exist")

        insert_sql = "insert into users(id,name,password,salt,role) values($1, $2, $3, $4, $5)"
        id = str(uuid.uuid1())
        encode_password = hashlib.sha1((password+salt).encode('utf8')).hexdigest()
        async with request.app.db.transaction(request) as cur:
            data = await cur.execute(insert_sql, id, name, encode_password, salt, "admin")
            if data:
                return RestStatus.response_status(201, "ok")
            else:
                return RestStatus.response_status(300, "save user fail")


class LoginMessage:

    async def get(self, request):
        return response.text("dage")


    def post(self, request):
        return response.text("nihao")


    def delete(self, request):
        return response.text("nihao")