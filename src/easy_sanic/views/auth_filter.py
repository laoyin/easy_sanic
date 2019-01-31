#coding=utf-8
import uuid
import hashlib
from sanic import response
from sanic.response import json

import settings
from utils.jwt_helper import JwtHelper
from utils.utils import generate_slat


class TokenFilter:

    async def get(self, request):
        headers = request.headers
        token = headers.get(settings.JWT_TOKEN_NAME)
        url = headers.get(settings.NEXT_URL, settings.xauth_login_api)
        with await request.app.conn as conn:
            # await conn.get("NOT_RESTRICT_URL") restrict
            url_status = await conn.execute('SISMEMBER', settings.xauth_api_allow_all, url)
            if url_status:
                return json(
                    {"parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string})

        toke_status, data = JwtHelper.validate(token)
        if toke_status:
            # 过滤权限
            user_role = data.get("role", "")
            service = url.replace("/", " ").strip().split(" ")[0]
            redis_role_key = settings.xauth_server_privileage.format(role=user_role, service=service)
            with await request.app.conn as conn:
                url_status = await conn.execute('SISMEMBER', redis_role_key, url)
                if url_status:
                    return json({"parsed": True, "args": request.args, "url": request.url,
                                 "query_string": request.query_string})
                else:
                    return response.text("Unauthorized", status=401)

        else:
            return response.text("forbidden", status=403)