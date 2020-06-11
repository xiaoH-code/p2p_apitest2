import logging

import requests,unittest
from api.login import login
from api.approve_api import approveAPI
from utils import assert_util


class test_approve(unittest.TestCase):
    phone = '13099881111'
    def setUp(self) -> None:
        self.login_api = login()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_approve_sucess(self):
        """实名认证成功"""
        #登录成功
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        #准备测试数据
        name = "张三"
        card_id = "110120202002021159"
        #发送实名认证请求
        response = self.approve_api.real_name_approve(self.session,name,card_id)
        logging.info("approve response={}".format(response.json()))
        assert_util(self,response,200,200,"提交成功!")

    def test02_approve_name_is_empty(self):
        """实名认证用户名为空，认证失败"""
        #登录成功
        response = self.login_api.login(self.session,self.phone,'test123')
        logging.info("login response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        #准备测试数据
        name = ""
        card_id = "110120202002021159"
        #发送实名认证请求
        response = self.approve_api.real_name_approve(self.session,name,card_id)
        logging.info("approve response={}".format(response.json()))
        assert_util(self,response,200,100,"姓名不能为空")

    def test03_id_is_empty(self):
        """实名认证身份证号为空，认证失败"""
        #登录成功
        response = self.login_api.login(self.session,self.phone,'test123')
        logging.info("login response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        #准备测试数据
        name = "张三"
        card_id = ""
        #发送实名认证请求
        response = self.approve_api.real_name_approve(self.session,name,card_id)
        logging.info("approve response={}".format(response.json()))
        assert_util(self,response,200,100,"身份证号不能为空")

    def test04_get_real_name_approve(self):
        """获取认证的身份信息"""
        # 登录成功
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_util(self, response, 200, 200, "登录成功")
        # 发送获取实名认证信息的请求
        response = self.approve_api.get_real_name_approve(self.session)
        logging.info("get_approve_info response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual('130****5678', response.json().get("phone"))