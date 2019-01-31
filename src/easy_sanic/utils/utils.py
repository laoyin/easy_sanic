#coding=utf-8
import string
import random
from sanic.response import json

__all__ = ["no_login_url"]

no_login_url = {
    "/login":"登录",
    "/index":"首页"
}


role_list_api ={
    "admin":["login", "search"],
    "weichat":["login"],
    "vip":["login", "search", "bug"]
}

def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    return [dict(r.items()) for r in records]



def generate_slat():
    letters = list(string.digits + string.ascii_letters)
    choiced_letters = random.choices(letters, k=6)
    return "".join(choiced_letters)



class RestStatus:

    @classmethod
    def response_status(cls, ret, message, data=""):
        return json({"ret": ret, "message": message, "data":data})