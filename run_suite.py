import time
import unittest
from lib.HTMLTestRunner_PY3 import HTMLTestRunner

#生成测试套件
import app
from script.test_approve import test_approve
from script.test_login_params import test_login
from script.test_tender import test_tender
from script.test_tender_process import test_tender_process
from script.test_trust import test_trust

suite = unittest.TestSuite()
#添加测试用例集合到测试套件中
suite.addTest(unittest.makeSuite(test_login))
suite.addTest(unittest.makeSuite(test_approve))
suite.addTest(unittest.makeSuite(test_trust))
suite.addTest(unittest.makeSuite(test_tender))
suite.addTest(unittest.makeSuite(test_tender_process))

#定义生成测试报告的路径
report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d %H%M%S"))

#使用HTMLTestRunner来生成测试报告
with open(report_file,mode='wb') as f:
    runner = HTMLTestRunner(f,title='测试输出接口测试报告',description="新版本报告模板")
    runner.run(suite)