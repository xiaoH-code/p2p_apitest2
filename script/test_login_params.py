import logging
import random
import time
import unittest

import requests
from parameterized import parameterized

import app
from api.login import login
from utils import assert_util, DButils, get_img_verify_code_data, get_register_data, read_data_file


class test_login(unittest.TestCase):
    def setUp(self) -> None:
        self.session = requests.Session()
        self.loginAPI = login()

    def tearDown(self) -> None:
        self.session.close()

    @classmethod
    def setUpClass(cls) -> None:
        sql1 = "delete from mb_member_register_log where phone in ('13099881111','13099881112','13099881113','13099881114');";
        DButils.execute_sql(sql1)
        logging.info('delete sql1 = {}'.format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13099881111','13099881112','13099881113','13099881114');";
        DButils.execute_sql(sql2)
        logging.info('delete sql1 = {}'.format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13099881111','13099881112','13099881113','13099881114');";
        DButils.execute_sql(sql3)
        logging.info('delete sql1 = {}'.format(sql3))
        sql4 = "delete from mb_member WHERE phone in ('13099881111','13099881112','13099881113','13099881114');";
        DButils.execute_sql(sql4)
        logging.info('delete sql1 = {}'.format(sql4))

    #读取定义的参数文件，并测试
    #@parameterized.expand(get_img_verify_code_data)
    @parameterized.expand(read_data_file('getImgCode.json','test_get_img_verify_code','type,statusCode'))
    def test01_get_img_verify_code(self,type,statusCode):
        # 输入测试数据
        if type == 'float':
            randNum = random.random()
        elif type == 'int':
            randNum = random.randint(1,10000000000)
        # 接收响应并断言
        response = self.loginAPI.getImgCode(self.session, randNum)
        logging.info("response = {}".format(response))
        self.assertEqual(statusCode,response.status_code)
        logging.info('modify')

    # #获取图片验证码，随机数为小数
    # @unittest.skip
    # def test01_get_img_verify_code_randomFloat(self):
    #     #输入测试数据
    #     randNum = random.random()
    #     #接收响应并断言
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #
    # #获取图片验证码，随机数为整数
    # @unittest.skip
    # def test02_get_img_verify_code_randomInt(self):
    #     # 输入测试数据
    #     randNum = random.randint(1,10000000000)
    #     # 接收响应并断言
    #     response = self.loginAPI.getImgCode(self.session, randNum)
    #     logging.info("response = {}".format(response))
    #     self.assertEqual(200,response.status_code)

    #正常获取获取短信验证码
    def test03_get_sms_verify_code_success(self):
        #先获取图片验证码
        randNum = random.random()
        response = self.loginAPI.getImgCode(self.session,randNum)
        self.assertEqual(200,response.status_code)
        #获取短信验证码
        response = self.loginAPI.getSmsCode(self.session,'13099881111','8888')
        print("sms_response = {}".format(response.json()))
        #断言短信验证码是否正确
        assert_util(self,response,200,200,"短信发送成功")

    #获取短信验证码-图片验证码错误
    def test04_get_sms_verify_code_imgCodeError(self):
        #先获取图片验证码
        randNum = random.random()
        response = self.loginAPI.getImgCode(self.session,randNum)
        self.assertEqual(200,response.status_code)
        #获取短信验证码——图片验证码错误
        response = self.loginAPI.getSmsCode(self.session,"13099881111",'1234')
        print("sms_response = {}".format(response.json()))
        #断言短信验证码是否正确
        assert_util(self, response, 200, 100, "图片验证码错误")

    #获取短信验证码 - 不调用获取图片验证码接口
    def test05_get_sms_verify_code_noImgCode(self):
        #未发送图片验证码，直接获取短信验证码
        response = self.loginAPI.getSmsCode(self.session,'13099881111','8888')
        print("sms_response = {}".format(response.json()))
        #断言短信验证码是否正确
        assert_util(self, response, 200, 100, "图片验证码错误")

    #测试注册功能相关的测试用例
    #@parameterized.expand(get_register_data)
    @parameterized.expand(read_data_file('register.json', 'register', 'phone,password,verifycode,phone_code,dy_server,statusCode,status,description'))
    def test06_register(self,phone,password,verifycode,phone_code,dy_server,statusCode,status,description):
        #先获取图片验证码
        randNum = random.random()
        response = self.loginAPI.getImgCode(self.session,randNum)
        self.assertEqual(200,response.status_code)
        #获取短信验证码
        response = self.loginAPI.getSmsCode(self.session,phone,'8888')
        logging.info("sms_response = {}".format(response.json()))
        #断言短信验证码是否正确
        assert_util(self,response,200,200,"短信发送成功")
        #发送注册请求
        response = self.loginAPI.register(self.session,phone,password,verifycode,phone_code,dy_server)
        logging.info("register response = {}".format(response.json()))
        assert_util(self,response,statusCode,status,description)

    # #注册成功
    # @unittest.skip
    # def test06_register_success(self):
    #     #先获取图片验证码
    #     randNum = random.random()
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #     #获取短信验证码
    #     response = self.loginAPI.getSmsCode(self.session,'13099881111','8888')
    #     print("sms_response = {}".format(response.json()))
    #     #断言短信验证码是否正确
    #     assert_util(self,response,200,200,"短信发送成功")
    #     #发送注册请求
    #     response = self.loginAPI.register(self.session,'13099881111')
    #     assert_util(self,response,200,200,"注册成功")
    #
    # #注册 - 手机号已存在
    # @unittest.skip
    # def test07_register_phoneIsExist(self):
    #     #先获取图片验证码
    #     randNum = random.random()
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #     #获取短信验证码
    #     response = self.loginAPI.getSmsCode(self.session,'13099881111','8888')
    #     print("sms_response = {}".format(response.json()))
    #     #断言短信验证码是否正确
    #     assert_util(self,response,200,200,"短信发送成功")
    #     #发送注册请求
    #     response = self.loginAPI.register(self.session,'13099881111')
    #     assert_util(self,response,200,100,"手机已存在!")
    #
    # #注册 - 密码为空
    # @unittest.skip
    # def test08_register_password_is_null(self):
    #     #先获取图片验证码
    #     randNum = random.random()
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #     #获取短信验证码
    #     response = self.loginAPI.getSmsCode(self.session,'13099881112','8888')
    #     print("sms_response = {}".format(response.json()))
    #     #断言短信验证码是否正确
    #     assert_util(self,response,200,200,"短信发送成功")
    #     #发送注册请求
    #     response = self.loginAPI.register(self.session,'13099881112',pwd='')
    #     assert_util(self,response,200,100,"密码不能为空")
    #
    # #注册 - 图片验证码错误
    # @unittest.skip
    # def test09_register_img_code_error(self):
    #     #先获取图片验证码
    #     randNum = random.random()
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #     #获取短信验证码
    #     response = self.loginAPI.getSmsCode(self.session,'13099881113','8888')
    #     logging.info("sms_response = {}".format(response.json()))
    #     #断言短信验证码是否正确
    #     assert_util(self,response,200,200,"短信发送成功")
    #     #发送注册请求
    #     response = self.loginAPI.register(self.session,'13099881113',imgCode='1234')
    #     logging.info("register_response = {}".format(response.json()))
    #     assert_util(self,response,200,100,"验证码错误!")
    #
    # #注册 - 短信验证码错误
    # @unittest.skip
    # def test10_register_sms_code_error(self):
    #     #先获取图片验证码
    #     randNum = random.random()
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #     #获取短信验证码
    #     response = self.loginAPI.getSmsCode(self.session,'13099881113','8888')
    #     logging.info("sms_response = {}".format(response.json()))
    #     #断言短信验证码是否正确
    #     assert_util(self,response,200,200,"短信发送成功")
    #     #发送注册请求
    #     response = self.loginAPI.register(self.session,'13099881113',phoneCode='111111')
    #     logging.info("register_response = {}".format(response.json()))
    #     assert_util(self,response,200,100,"验证码错误")
    #
    # #注册 - 不同意协议
    # @unittest.skip
    # def test11_register_no_premission_protocol(self):
    #     #先获取图片验证码
    #     randNum = random.random()
    #     response = self.loginAPI.getImgCode(self.session,randNum)
    #     self.assertEqual(200,response.status_code)
    #     #获取短信验证码
    #     response = self.loginAPI.getSmsCode(self.session,'13099881113','8888')
    #     logging.info("sms_response = {}".format(response.json()))
    #     #断言短信验证码是否正确
    #     assert_util(self,response,200,200,"短信发送成功")
    #     #发送注册请求
    #     response = self.loginAPI.register(self.session,'13099881113',agree='off')
    #     logging.info("register_response = {}".format(response.json()))
    #     assert_util(self,response,200,100,"请同意我们的条款")

    def test13_login_success(self):
        """登录成功"""
        #发送登录请求
        response = self.loginAPI.login(self.session)
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,200,"登录成功")

    def test14_username_is_not_exist(self):
        """用户名不存在"""
        #发送登录请求
        response = self.loginAPI.login(self.session,kw='13099212314')
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,100,"用户不存在")

    def test15_password_is_empty(self):
        """密码不能为空"""
        #发送登录请求
        response = self.loginAPI.login(self.session,pwd='')
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,100,"密码不能为空")

    def test16_login_password_wrong(self):
        """多次密码错误时提示"""
        #第一次输入错误密码
        response = self.loginAPI.login(self.session,pwd='error')
        logging.info("密码错误1次，响应为：{}".format(response.json()))
        assert_util(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        # 第二次输入错误密码
        response = self.loginAPI.login(self.session, pwd='error')
        logging.info("密码错误2次，响应为：{}".format(response.json()))
        assert_util(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        # 第三次输入错误密码
        response = self.loginAPI.login(self.session, pwd='error')
        logging.info("密码错误3次，响应为：{}".format(response.json()))
        assert_util(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #登录-输入3次错误后再输入正确密码
        response = self.loginAPI.login(self.session)
        logging.info("密码错误3次后输入正确密码登录，响应为：{}".format(response.json()))
        assert_util(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #登录60s发送登录请求，登录成功
        time.sleep(60)
        #发送登录请求
        response = self.loginAPI.login(self.session)
        logging.info("密码错误3次后等待60秒，输入正确密码登录，响应为：{}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")

    def test17_is_login_nologin(self):
        """未登录时判定是否登录"""
        #发送判断请求
        response = self.loginAPI.islogin(self.session)
        logging.info("islogin response={}".format(response.json()))
        #断言
        assert_util(self,response,200,250,"您未登陆！")

    def test18_is_login(self):
        """登录时判定是否登录"""
        #发送登录请求
        response = self.loginAPI.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        #判断是否登录
        response = self.loginAPI.islogin(self.session)
        logging.info("islogin response={}".format(response.json()))
        assert_util(self,response,200,200,"OK")