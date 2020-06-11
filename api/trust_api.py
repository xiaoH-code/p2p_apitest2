import random

import app


class trustAPI():
    def __init__(self):
        self.trust_register_url = app.BASE_URL + '/trust/trust/register'
        self.get_recharge_code_url = app.BASE_URL + '/common/public/verifycode/'
        self.recharge_url = app.BASE_URL + '/trust/trust/recharge'

    def trust_register(self,session):
        response = session.post(self.trust_register_url)
        return response

    def get_recharge_code(self,session):
        #定义参数
        r = random.random()
        url = self.get_recharge_code_url + str(r)
        #发送获取验证码的请求
        response = session.get(url)
        return response

    def recharge(self,session,amount,valicode='8888'):
        #定义参数
        data = {"paymentType": "chinapnrTrust", "formStr": "reForm", "amount": amount, "valicode": valicode}
        response = session.post(self.recharge_url,data=data)
        return response
