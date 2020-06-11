import app

class approveAPI():
    def __init__(self):
        self.real_name_approve_url = app.BASE_URL + "/member/realname/approverealname"
        self.get_approve_url = app.BASE_URL + "/member/member/getapprove"

    def real_name_approve(self,session,realname,card_id):
        data = {"realname": realname, "card_id": card_id}
        response = session.post(self.real_name_approve_url,data=data,files={'x':'y'})
        return response

    def get_real_name_approve(self,session):
        response = session.post(self.get_approve_url)
        return  response