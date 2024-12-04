# coding=utf-8
import time

from common.Base import Base
from utils.Logutil import logger
from utils.Readmysql import RdTestcase
from utils.Requestsutil import RequestSend
from common.InterfaceDetail import InterfaceDetail
case_data = RdTestcase()

title = ''
environment = 'main'
path = '/pro/v1/todo/deleteBatch'
# request_body = \
# '{"corpid":"ding66041eb1c6df73f535c2f4657eb6378f","userId":"215252650523902241","platform":"web","businessType":21500,"dataIdList":[132]}'
res_data = None
conf_key = case_data.loadConfkey('xbb', environment)
url = conf_key['value'] + path
headers = eval(conf_key['headers'])
method = 'post'
# data = eval(request_body)
case_name = title
bs = InterfaceDetail()
# data = base.get_data(data)
# headers = base.get_headers(data, headers)


for i in range(132033, 132156):
    # logger.info("正在执行{}用例".format(case_name))
    request_body = '{"corpid":"ding66041eb1c6df73f535c2f4657eb6378f","userId":"215252650523902241","platform":"web","businessType":21500,"dataIdList":[' + str(i) +']}'
    conf_key = case_data.loadConfkey('xbb', environment)
    url = conf_key['value'] + path
    headers = eval(conf_key['headers'])
    data = eval(request_body)

    # 更新数据中的登录信息
    key_map = {'corpid': '', 'userId': ''}
    data = bs.update_data_with_login_info(data, key_map)

    # 添加签名到请求头
    headers = bs.get_headers(data, headers)

    try:
        logger.info(f"正在执行 {case_name} 用例")
        res_data = RequestSend().send(url, method, data=data, headers=headers)
        logger.info(f"用例执行成功，请求的结果为\n\t{res_data}")
    except Exception as e:
        logger.error(f"用例执行失败，请查看日志。错误信息: {e}")
        assert False