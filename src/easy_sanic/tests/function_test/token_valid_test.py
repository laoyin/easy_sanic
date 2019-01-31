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


class ValidTokenRequest(unittest.TestCase):

    def setUp(self):
        self.token = JwtHelper.generate_token()

    def testValid(self):
        self.assertTrue(JwtHelper.validate(self.token)[0], True)


    def testExperationDateValid(self):
        self.token = JwtHelper.generate_token(iss='aegis.com', exp=60)
        self.assertTrue(JwtHelper.validate(self.token)[0], True)
        print("测试通过， jwttoken 生成 以及验证")
        time.sleep(60)
        print("测试token 过期")
        self.assertTrue(JwtHelper.validate(self.token)[0], False)



if __name__ == "__main__":
    unittest.main()