import logging
import unittest

import requests
from bs4 import BeautifulSoup

from api.trust_api import trustAPI
from api.login import login
from utils import assert_util, third_party_request


class test_trust(unittest.TestCase):
    def setUp(self) -> None:
        self.trust_api = trustAPI()
        self.login_api = login()
        self.session = requests.session()
        #0、登录
        response = self.login_api.login(self.session)
        logging.info('login response = {}'.format(response.json()))
        assert_util(self,response,200,200,'登录成功')

    def tearDown(self) -> None:
        self.session.close()

    def test01_trust_register(self):
        #发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info('trust response = {}'.format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))

        #提取开户请求的响应中的HTML内容
        html_data = response.json().get("description").get("form")
        # #发送第三方请求
        response = third_party_request(self.session,html_data)
        logging.info('third request reposne = {}'.format(response.text))
        self.assertEqual(200,response.status_code)
        self.assertEqual('UserRegister OK',response.text)

    def test02_recharge(self):
        #1、获取充值验证码
        response = self.trust_api.get_recharge_code(self.session)
        #logging.info('get_recharge_code_response = {}'.format(response.text))
        self.assertEqual(200,response.status_code)
        #2、充值（1000元）
        response = self.trust_api.recharge(self.session,'1000')
        logging.info('recharge response = {}'.format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        #3、调用第三方充值接口
        #3.1获取充值响应中的HMTL数据
        html_data = response.json().get("description").get("form")
        #3.2提取第三方请求的URL和参数，并发送请求
        response = third_party_request(self.session,html_data)
        #3.5断言第三方请求是否成功
        self.assertEqual(200,response.status_code)
        self.assertEqual('NetSave OK',response.text)