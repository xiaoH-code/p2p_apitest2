import logging
import random

import requests,unittest
from api.login import login
from api.tender_api import tenderAPI
from api.trust_api import trustAPI
from utils import assert_util, third_party_request


class test_tender_process(unittest.TestCase):
    phone = '13099881114'
    tender_id = 249
    imVerifyCode = '8888'

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = login()
        cls.tender_api = tenderAPI()
        cls.trust_api = trustAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    def test01_register_success(self):
        # 请求图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone, self.imVerifyCode)
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.register(self.session, self.phone, 'test123')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_util(self, response, 200, 200, "注册成功")

    def test02_login_success(self):
        """登录成功"""
        #发送登录请求
        response = self.login_api.login(self.session,self.phone, 'test123')
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,200,"登录成功")

    def test03_trust_success(self):
        """开户"""
        #发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("trust respone = {}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        #提取开户请求的响应中的HTML内容
        html_data = response.json().get("description").get("form")
        # #发送第三方请求
        response = third_party_request(self.session,html_data)
        logging.info('third request reposne = {}'.format(response.text))
        self.assertEqual(200,response.status_code)
        self.assertEqual('UserRegister OK',response.text)

    def test04_recharge_success(self):
        """充值"""
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

    def test05_get_loaninfo(self):
        """获取投资产品详情"""
        #请求投资产品的详情
        response = self.tender_api.get_loaninfo(self.session,self.tender_id)
        logging.info("get_tender response = {}".format(response.json()))
        #断言投资详情是否正确
        assert_util(self,response,200,200,"OK")
        self.assertEqual(str(self.tender_id),response.json().get("data").get("loan_info").get("id"))

    def test06_tender(self):
        #投资
        #发送投资请求
        amount = '100'
        response = self.tender_api.tender(self.session,self.tender_id,amount)
        logging.info("tender response = {}".format(response.json()))
        #断言投资结果是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = third_party_request(self.session,form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('InitiativeTender OK', response.text)

    def test07_get_tenderlist(self):
        """获取我的投资列表"""
        status = "tender"
        #发送获取投资列表的请求
        response = self.tender_api.get_tenderlist(self.session,status)
        logging.info("get_tender response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)