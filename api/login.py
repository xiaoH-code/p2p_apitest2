import app

class login():
    def __init__(self):
        self.get_img_verify_code_url = app.BASE_URL + '/common/public/verifycode1/'
        self.get_sms_verify_code_url = app.BASE_URL + '/member/public/sendSms'
        self.register_url = app.BASE_URL + '/member/public/reg'
        self.login_url = app.BASE_URL + '/member/public/login'
        self.islogin_url = app.BASE_URL + '/member/public/islogin'

    def getImgCode(self,session,randnum):
        url = self.get_img_verify_code_url + str(randnum)
        response = session.get(url)
        return response

    def getSmsCode(self,session,phone,imgCode):
        data = {"phone": phone, "imgVerifyCode": imgCode, "type": "reg"}
        response = session.post(self.get_sms_verify_code_url, data=data)
        return response

    def register(self,session,phone,pwd="test123",imgCode="8888",phoneCode="666666",agree = "on"):
        data = {"phone": phone,"password": pwd,"verifycode": imgCode,"phone_code": phoneCode,"dy_server": agree}
        response = session.post(self.register_url,data=data)
        return response

    def login(self,session,kw='13012345678',pwd='test123'):
        data = {"keywords": kw,"password": pwd}
        response = session.post(self.login_url,data=data)
        return response

    def islogin(self,session):
        response = session.post(self.islogin_url)
        return response