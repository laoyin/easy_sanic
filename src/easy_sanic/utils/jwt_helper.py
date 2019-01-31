#coding=utf-8
import jwt
import time

import settings

class JwtHelper(object):

    @classmethod
    def validate(cls, token):
        try:
            print(token)
            payload = jwt.decode(token, settings.JWT_SECRET,  audience='www.aegis.com', algorithms=['HS256'])
        except Exception as e:
            print(e)
            return False, None
        if payload:
            exp = payload["exp"]
            if time.time() > int(exp):
                return False, payload
            return True, payload
        else:
            return True, None


    @classmethod
    def generate_token(cls, iss='aegis.com', iat=int(time.time()), exp=3600):

        payload = {
            "iss":iss,
            "iat":iat,
            "exp":iat+exp,
            "aud":"www.aegis.com",
            "sub":"yin",
            "user":"yin",
            "role":"admin"
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
        return token