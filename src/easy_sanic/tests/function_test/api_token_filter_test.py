#coding=utf-8
"""
@author yxp
"""
import requests
import unittest
import os
import sys
import time
SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.extend([SRC_DIR])
from utils.jwt_helper import JwtHelper
import settings


class ValidTokenRequest(unittest.TestCase):

    def setUp(self):
        self.httphelper = requests
        self.token = JwtHelper.generate_token(iss='aegis.com', exp=600)

    def testInvalid(self):
        self.assertNotEqual(requests.get("http://127.0.0.1:7001/token").status_code, 200)

    def testValid(self):
        headers = {
            settings.JWT_TOKEN_NAME:self.token
        }
        self.assertEqual(requests.get("http://127.0.0.1:7001/token", headers=headers).status_code, 200)


if __name__ == "__main__":
    unittest.main()