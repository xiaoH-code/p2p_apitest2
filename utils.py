import json
import logging

import pymysql
from bs4 import BeautifulSoup

import app


def assert_util(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

class DButils:
    @classmethod
    def get_conn(cls):
        conn = pymysql.connect(app.DB_host,app.DB_user,app.DB_password,app.database_mem,autocommit=True)
        return conn

    @classmethod
    def close_conn(cls,cursor = None,conn = None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def execute_sql(cls,sql):
        try:
            conn = cls.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close_conn()

def third_party_request(session,html_data):
    # 初始化Bs4的对象
    soup = BeautifulSoup(html_data, 'html.parser')
    # 提取第三方请求的URL
    third_request_url = soup.form['action']
    # 提取第三方请求的参数名和参数值
    json_para = {}
    for params in soup.find_all('input'):
        json_para.setdefault(params.get("name"), params.get("value"))
    logging.info('params = {}'.format(json_para))
    # 发送第三方请求
    response = session.post(third_request_url, data=json_para)
    return response

def get_img_verify_code_data():
    test_data = []
    #读取数据文件
    file_path = app.BASE_DIR + '/data/getImgCode.json'
    #将数据文件中的内容读取到参数中
    with open(file_path,'r',encoding='utf-8') as f:
        json_data = json.load(f)
        data_list = json_data.get('test_get_img_verify_code')
        for case_data in data_list:
            test_data.append((case_data.get("type"),case_data.get('statusCode')))
    print(test_data)
    return test_data

def get_register_data():
    test_data = []
    #数据文件路径
    file_path = app.BASE_DIR + '/data/register.json'
    #将数据文件中的内容读取到参数中
    with open(file_path,'r',encoding='utf-8') as f:
        json_data = json.load(f)
        data_list = json_data.get('register')
        for case_data in data_list:
            test_data.append((case_data.get('phone'),case_data.get('password'),case_data.get('verifycode'),case_data.get('phone_code'),case_data.get('dy_server'),case_data.get('statusCode'),case_data.get('status'),case_data.get('description')))
    print(test_data)
    return test_data

def read_data_file(filename,module_name,lists):
    test_data = []
    #数据文件的路径
    file_path = app.BASE_DIR + '/data/' + filename
    #将数据文件中的内容读取到参数中
    with open(file_path,'r',encoding='utf-8') as f:
        json_data = json.load(f)
        data_list = json_data.get(module_name)
        for case_data in data_list:
            test_case_data = []
            for param in lists.split(','):
                test_case_data.append(case_data.get(param))
            test_data.append(test_case_data)
    logging.info(test_data)
    return test_data